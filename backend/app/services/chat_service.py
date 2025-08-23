import os
from typing import Dict, List, Literal, Optional, Annotated
from typing_extensions import TypedDict
from sqlalchemy import text

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.prompts import PromptTemplate

from app.config.database import get_db
from app.utils.gemini_client import generate_embeddings
from app.models.url_company import UrlCompany

class ChatState(TypedDict):
    """
    State untuk chat workflow.
    Kunci 'messages' akan menyimpan seluruh riwayat percakapan.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    
    company_id: int
    
    retrieval_context: Optional[str]
    web_search_context: Optional[str]
    need_web_search: bool

class LangGraphChatService:
    def __init__(self):
        self.model_name = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        self.memory = MemorySaver()
        
        self.graph = self._build_graph()

    def _get_company_domains(self, company_id: int) -> List[str]:
        db = next(get_db())
        try:
            urls = (
                db.query(UrlCompany.url)
                .filter(UrlCompany.company_id == company_id)
                .all()
            )
            formatted_urls = [url[0] for url in urls]
            return formatted_urls
        except Exception as e:
            print("Error:", e)
        finally:
            db.close()
        return []

    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(ChatState)
        
        workflow.add_node("retrieval", self._retrieval_node)
        workflow.add_node("check_relevance", self._check_relevance_node)
        workflow.add_node("web_search", self._web_search_node)
        workflow.add_node("generate_response", self._generate_response_node)
        
        workflow.add_edge(START, "retrieval")
        workflow.add_edge("retrieval", "check_relevance")
        workflow.add_conditional_edges(
            "check_relevance",
            self._route_after_relevance_check,
            {"web_search": "web_search", "generate": "generate_response"}
        )
        workflow.add_edge("web_search", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile(checkpointer=self.memory)


    def _retrieval_node(self, state: ChatState) -> Dict:
        """Node untuk melakukan retrieval dari database"""

        user_query = state["messages"][-1].content
        company_id = state["company_id"]
        
        query_embedding = generate_embeddings([user_query])[0]
        db = next(get_db())
        try:
            sql_query = text("""
                SELECT chunk_content FROM doc_embeddings
                WHERE company_id = :company_id
                ORDER BY embedding <-> :query_embedding LIMIT 3
            """)
            results = db.execute(sql_query, {
                "company_id": company_id,
                "query_embedding": str(query_embedding)
            }).fetchall()
            
            retrieval_context = ""
            if results:
                retrieval_context = "\n\n".join([
                    f"[Dokumen Internal {i+1}]: {row[0]}" for i, row in enumerate(results)
                ])
            
            return {"retrieval_context": retrieval_context}
        finally:
            db.close()


    def _check_relevance_node(self, state: ChatState) -> Dict:
        """Node untuk mengecek relevansi konteks yang ditemukan"""
        user_query = state["messages"][-1].content
        retrieval_context = state["retrieval_context"]
        
        if not retrieval_context or retrieval_context.strip() == "":
            return {"need_web_search": True}
        
        relevance_prompt = f"""
        Nilai apakah konteks berikut dapat menjawab pertanyaan pengguna.
        Pertanyaan: {user_query}
        Konteks:\n{retrieval_context}
        Jawab HANYA dengan 'RELEVAN' atau 'TIDAK_RELEVAN'.
        Jawaban:"""
        
        relevance_response = self.llm.invoke([HumanMessage(content=relevance_prompt)])
        relevance_decision = relevance_response.content.strip().upper()
        need_web_search = "TIDAK_RELEVAN" in relevance_decision
        
        return {"need_web_search": need_web_search}


    def _route_after_relevance_check(self, state: ChatState) -> Literal["web_search", "generate"]:
        """Router untuk menentukan apakah perlu web search atau langsung generate"""
        if state["need_web_search"]:
            return "web_search"
        return "generate"


    def _web_search_node(self, state: ChatState) -> Dict:
        """Node untuk melakukan web search"""
        user_query = state["messages"][-1].content
        company_id = state["company_id"]
        company_domains = self._get_company_domains(company_id)
        
        try:
            tavily_search = TavilySearch(
                tavily_api_key=os.getenv("TAVILY_API_KEY"),
                include_answer=True, max_results=1,
                include_domains=company_domains if company_domains else None,
            )
            search_response = tavily_search.invoke({"query": user_query})
            
            web_context = ""
            if isinstance(search_response, dict):
                 if search_response.get("answer"):
                     web_context += f"Ringkasan Jawaban: {search_response['answer']}\n\n"
                 if search_response.get("results"):
                     for result in search_response["results"]:
                         web_context += f"[{result['title']}]({result['url']})\n"
                        #  web_context += f"{result['content'][:500]}...\n\n"
                     pass 
                 
            return {"web_search_context": web_context if web_context else None}
        except Exception as e:
            print(f"Error in web search: {e}")
            return {"web_search_context": "Maaf, terjadi kesalahan saat mencari informasi online."}


    def _generate_response_node(self, state: ChatState) -> Dict:
        """Node untuk generate response final berdasarkan riwayat dan konteks."""
        user_query = state["messages"][-1].content
        conversation_history = state["messages"]
        retrieval_context = state.get("retrieval_context", "Tidak ada.")
        web_search_context = state.get("web_search_context", "Tidak ada.")


        prompt_template = """
        Anda adalah asisten customer service yang profesional dan ramah. Tugas Anda adalah membantu pelanggan berdasarkan informasi yang tersedia dalam knowledge base perusahaan.

        RIWAYAT PERCAKAPAN:
        {history}

        KONTEKS DARI DOKUMEN INTERNAL:
        {context}

        KONTEKS DARI WEB SEARCH:
        {web_context}
        
        PERTANYAAN PENGGUNA SAAT INI: {question}
        
        PEDOMAN MENJAWAB:
        1. Selalu awali dengan sapaan yang ramah.
        2. Gunakan informasi dari riwayat percakapan dan konteks yang diberikan untuk menjawab pertanyaan.
        3. Jika Konteks tidak memiliki informasi yang cukup, jelaskan dengan sopan bahwa anda tidak memiliki informasi yang cukup untuk menjawab pertanyaan pelanggan dan arahkan pelanggan untuk menghubungi support manusia.
        4. Jangan pernah menyebutkan bahwa anda menggunakan informasi tambahan untuk menjawab pertanyaan pelanggan.

        JAWABAN ANDA:"""
        
        prompt = PromptTemplate.from_template(prompt_template)
        
        formatted_history = "\n".join(
            [f"{'Pengguna' if isinstance(msg, HumanMessage) else 'Asisten'}: {msg.content}" for msg in conversation_history[:-1]]
        )

        formatted_prompt = prompt.format(
            history=formatted_history,
            context=retrieval_context,
            web_context=web_search_context,
            question=user_query
        )
        
        response = self.llm.invoke([HumanMessage(content=formatted_prompt)])
        
        return {"messages": [AIMessage(content=response.content)]}


    async def process_message(self, company_id: int, thread_id: str, message: str) -> str:
        """
        Metode utama untuk memproses pesan chat, kini memerlukan thread_id.
        """
        config = {"configurable": {"thread_id": thread_id}}
        
        input_data = {
            "messages": [HumanMessage(content=message)],
            "company_id": company_id
        }
        
        final_response_content = ""
        async for event in self.graph.astream(input_data, config=config):
            if "generate_response" in event:
                ai_message = event["generate_response"]["messages"][-1]
                final_response_content = ai_message.content
        
        return final_response_content

langgraph_chat_service = LangGraphChatService()

async def process_chat_message_langgraph(company_id: int, thread_id: str, message: str) -> str:
    return await langgraph_chat_service.process_message(company_id, thread_id, message)