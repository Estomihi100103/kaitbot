from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
import json
import os 


logger = logging.getLogger(__name__)


EMBEDDING_CHUNK_SIZE = int(os.getenv('EMBEDDING_CHUNK_SIZE', 1024))
EMBEDDING_CHUNK_OVERLAP = int(os.getenv('EMBEDDING_CHUNK_OVERLAP', 200))
MAX_CHARS_PER_LLM_CALL = 30000


def generate_contextual_chunks(text: str, model: str = "models/gemini-2.5-flash-lite") -> str:
    """
    Memecah teks menjadi chunk kontekstual menggunakan LLM.
    Jika teks terlalu panjang, proses akan dilakukan dalam beberapa batch.
    """
    print("use generate_contextual_chunks")
    model_name = os.getenv("GEMINI_TEXT_MODEL", "models/gemini-2.5-flash-lite")
    llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=os.getenv("GEMINI_API_KEY"))
    
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Tugas kamu adalah MEMECAH teks panjang menjadi beberapa *chunk* yang bermakna secara SEMANTIK.

        Ikuti aturan berikut DENGAN KETAT:

        1. Panjang SETIAP chunk:
        - MINIMAL: 256 karakter
        - MAKSIMAL: 1024 karakter
        - Jangan ada chunk yang melebihi batas ini.
        2. Fokus UTAMA: Setiap chunk harus fokus pada SATU TOPIK SAJA sehingga konteks tetap terjaga.
        3. Jika SATU topik terlalu panjang:
        - LANJUTKAN ke chunk berikutnya.
        - AWALI chunk lanjutan dengan kalimat penghubung PENJAGA KONTEKS, agar alur tetap nyambung.
        4. Buat JUMLAH chunk SECUKUPNYA. Jangan memecah terlalu banyak atau terlalu sedikit.
        5. Setiap chunk WAJIB memenuhi batas panjang yang disebutkan di poin 1.

        HASILKAN output dalam format **JSON MURNI** dengan struktur berikut - tanpa penjelasan, tanpa kata pengantar, tanpa teks tambahan apa pun:

        [
        {{"chunk_id": 1, "content": "isi chunk pertama"}},
        {{"chunk_id": 2, "content": "isi chunk kedua"}},
        ...
        ]

        BERIKUT TEKSNYA: {text}"""
    )
    
    if len(text) <= MAX_CHARS_PER_LLM_CALL:
        formatted_prompt = prompt.format(text=text, chunk_size=EMBEDDING_CHUNK_SIZE)
        response = llm.invoke(formatted_prompt)
        return response.content
    else:
        batch_splitter = RecursiveCharacterTextSplitter(
            chunk_size=MAX_CHARS_PER_LLM_CALL,
            chunk_overlap=100  
        )
        text_batches = batch_splitter.split_text(text)
        
        all_chunks = []
        
        for batch in text_batches:
            formatted_prompt = prompt.format(text=batch)
            
            try:
                response = llm.invoke(formatted_prompt)
                cleaned_response = response.content.strip().replace('```json', '').replace('```', '')
                chunks_from_batch = json.loads(cleaned_response)
                all_chunks.extend(chunks_from_batch)
            except (json.JSONDecodeError, AttributeError) as e:
                continue
            
        return json.dumps(all_chunks, indent=2, ensure_ascii=False)


def overlap_chunk_texts(full_text: str):
    print("use overlap_chunk_texts")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=EMBEDDING_CHUNK_SIZE,
        chunk_overlap=EMBEDDING_CHUNK_OVERLAP,
    )
    return splitter.split_text(full_text)

