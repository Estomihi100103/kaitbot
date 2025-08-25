from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.company import Company
from app.services.chat_service import process_chat_message_langgraph
from pydantic import BaseModel
import uuid
from datetime import datetime
import os
from app.models.conversation import Conversation, Message, MessageSender

router = APIRouter(tags=["chatbot"])

class ChatRequest(BaseModel):
    message: str
    thread_id: str


@router.get("/config/{company_slug}", response_model=dict)
async def get_widget_config(company_slug: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    style_config = company.style_config or {"primaryColor": "#007bff", "position": "bottom-right"}
    greeting_message = company.greeting_message or "Halo! Bagaimana saya bisa membantu Anda?"

    return {
        "companyName": company.name,
        "greetingMessage": greeting_message,
        "style": {
            "primaryColor": style_config.get("primaryColor", "#007bff"),
            "position": style_config.get("position", "bottom-right")
        }
    }


@router.get("/embed/{company_slug}.js", response_class=PlainTextResponse)

async def get_embed_js(
    company_slug: str, 
    request: Request, 
    db: Session = Depends(get_db)
):
    
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    base_url = f"{request.url.scheme}://{request.headers['host']}"
    api_url = f"{base_url}/api/v1/chatbot"
    
    js_content = f"""
(async () => {{
    try {{
        const companySlug = '{company_slug}';
        const API_URL = '{api_url}';
        
        let threadId = localStorage.getItem(`chatbot_thread_id_${{companySlug}}`);
        if (!threadId) {{
            threadId = crypto.randomUUID(); 
            localStorage.setItem(`chatbot_thread_id_${{companySlug}}`, threadId);
        }}
        
        // Ambil konfigurasi dari backend
        const response = await fetch(`${{API_URL}}/config/${{companySlug}}`);
        if (!response.ok) throw new Error('Failed to fetch config');
        const config = await response.json();
        
        // Container utama untuk memastikan z-index
        const chatbotContainer = document.createElement('div');
        chatbotContainer.style.zIndex = '1000';
        document.body.appendChild(chatbotContainer);
        
        // Buat chat bubble dengan animasi
        const bubble = document.createElement('div');
        bubble.style.position = 'fixed';
        bubble.style.bottom = '20px';
        bubble.style.right = '20px';
        bubble.style.width = '60px';
        bubble.style.height = '60px';
        bubble.style.borderRadius = '50%';
        bubble.style.backgroundColor = config.style.primaryColor;
        bubble.style.color = '#fff';
        bubble.style.display = 'flex';
        bubble.style.alignItems = 'center';
        bubble.style.justifyContent = 'center';
        bubble.style.cursor = 'pointer';
        bubble.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
        bubble.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
        bubble.innerHTML = '💬';
        bubble.addEventListener('mouseover', () => {{
            bubble.style.transform = 'scale(1.1)';
            bubble.style.boxShadow = '0 6px 16px rgba(0,0,0,0.4)';
        }});
        bubble.addEventListener('mouseout', () => {{
            bubble.style.transform = 'scale(1)';
            bubble.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
        }});
        chatbotContainer.appendChild(bubble);
        
        // Buat chat window dengan animasi
        const chatWindow = document.createElement('div');
        chatWindow.style.position = 'fixed';
        chatWindow.style.bottom = '90px';
        chatWindow.style.right = '20px';
        chatWindow.style.width = '320px';
        chatWindow.style.height = '450px';
        chatWindow.style.backgroundColor = '#fff';
        chatWindow.style.borderRadius = '12px';
        chatWindow.style.display = 'none';
        chatWindow.style.flexDirection = 'column';
        chatWindow.style.boxShadow = '0 8px 24px rgba(0,0,0,0.2)';
        chatWindow.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        chatWindow.style.opacity = '0';
        chatWindow.style.transform = 'translateY(20px)';
        chatWindow.style.zIndex = '1002';
        chatbotContainer.appendChild(chatWindow);
        
        // Header chat dengan tombol tutup
        const header = document.createElement('div');
        header.style.backgroundColor = config.style.primaryColor;
        header.style.color = '#fff';
        header.style.padding = '12px 16px';
        header.style.borderTopLeftRadius = '12px';
        header.style.borderTopRightRadius = '12px';
        header.style.display = 'flex';
        header.style.alignItems = 'center';
        header.style.justifyContent = 'space-between';
        header.innerHTML = `
            <div style="display: flex; align-items: center;">
                <span style="font-size: 24px; margin-right: 8px;">🤖</span>
                <strong>${{config.companyName || 'Chatbot'}}</strong>
            </div>
        `;
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '✕';
        closeBtn.style.background = 'none';
        closeBtn.style.border = 'none';
        closeBtn.style.color = '#fff';
        closeBtn.style.fontSize = '16px';
        closeBtn.style.cursor = 'pointer';
        closeBtn.style.padding = '4px 8px';
        closeBtn.addEventListener('click', () => {{
            chatWindow.style.display = 'none';
        }});
        header.appendChild(closeBtn);
        chatWindow.appendChild(header);
        
        // Area pesan dengan styling modern
        const messageArea = document.createElement('div');
        messageArea.style.flex = '1';
        messageArea.style.padding = '16px';
        messageArea.style.overflowY = 'auto';
        messageArea.style.backgroundColor = '#f8f9fa';
        messageArea.style.borderBottom = '1px solid #e0e0e0';
        chatWindow.appendChild(messageArea);
        
        // Input area dengan tombol kirim
        const inputArea = document.createElement('div');
        inputArea.style.padding = '12px';
        inputArea.style.display = 'flex';
        inputArea.style.alignItems = 'center';
        inputArea.style.backgroundColor = '#fff';
        inputArea.style.borderBottomLeftRadius = '12px';
        inputArea.style.borderBottomRightRadius = '12px';
        
        const input = document.createElement('textarea');
        input.placeholder = 'Ketik pesan...';
        input.style.flex = '1';
        input.style.padding = '10px';
        input.style.border = '1px solid #ddd';
        input.style.borderRadius = '8px';
        input.style.marginRight = '8px';
        input.style.outline = 'none';
        input.style.resize = 'none';
        input.style.height = '40px';
        input.style.maxHeight = '100px';
        input.style.overflowY = 'auto';
        inputArea.appendChild(input);
        
        const sendBtn = document.createElement('button');
        sendBtn.innerHTML = '➤';
        sendBtn.style.backgroundColor = config.style.primaryColor;
        sendBtn.style.color = '#fff';
        sendBtn.style.border = 'none';
        sendBtn.style.borderRadius = '8px';
        sendBtn.style.padding = '10px';
        sendBtn.style.cursor = 'pointer';
        sendBtn.style.transition = 'background-color 0.3s ease';
        sendBtn.addEventListener('mouseover', () => {{
            sendBtn.style.backgroundColor = '#0056b3';
        }});
        sendBtn.addEventListener('mouseout', () => {{
            sendBtn.style.backgroundColor = config.style.primaryColor;
        }});
        inputArea.appendChild(sendBtn);
        chatWindow.appendChild(inputArea);
        
        // Toggle chat window dengan animasi
        bubble.addEventListener('click', () => {{
            if (chatWindow.style.display === 'none') {{
                chatWindow.style.display = 'flex';
                setTimeout(() => {{
                    chatWindow.style.opacity = '1';
                    chatWindow.style.transform = 'translateY(0)';
                }}, 10);
            }} else {{
                chatWindow.style.opacity = '0';
                chatWindow.style.transform = 'translateY(20px)';
                setTimeout(() => {{
                    chatWindow.style.display = 'none';
                }}, 300);
            }}
        }});
        
        // Fungsi untuk menambahkan pesan
        const addMessage = (text, isUser = false) => {{
            const msgDiv = document.createElement('div');
            msgDiv.style.marginBottom = '12px';
            msgDiv.style.display = 'flex';
            msgDiv.style.alignItems = 'flex-start';
            msgDiv.style.flexDirection = isUser ? 'row-reverse' : 'row';
            
            const avatar = document.createElement('div');
            avatar.innerHTML = isUser ? '👤' : '🤖';
            avatar.style.fontSize = '20px';
            avatar.style.margin = isUser ? '0 0 0 8px' : '0 8px 0 0';
            
            const msgSpan = document.createElement('span');
            msgSpan.innerHTML = text.replace(/\\n/g, '<br>');
            msgSpan.style.padding = '10px 14px';
            msgSpan.style.borderRadius = '12px';
            msgSpan.style.backgroundColor = isUser ? '#e6f3ff' : '#f0f0f0';
            msgSpan.style.maxWidth = '70%';
            msgSpan.style.lineHeight = '1.4';
            msgSpan.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
            
            msgDiv.appendChild(avatar);
            msgDiv.appendChild(msgSpan);
            messageArea.appendChild(msgDiv);
            messageArea.scrollTop = messageArea.scrollHeight;
        }};
        
        // Kirim pesan
        const sendMessage = async () => {{
            if (!input.value.trim()) return;
            const message = input.value;
            input.value = '';
            input.style.height = '40px'; // Reset tinggi textarea
            
            // Tampilkan pesan pengguna
            addMessage(message, true);
            
            // Tampilkan typing indicator
            const typingDiv = document.createElement('div');
            typingDiv.style.marginBottom = '12px';
            typingDiv.style.display = 'flex';
            typingDiv.style.alignItems = 'center';
            typingDiv.innerHTML = '<span style="margin-right: 8px;">🤖</span><span style="padding: 8px; font-style: italic; color: #666;">Typing...</span>';
            messageArea.appendChild(typingDiv);
            messageArea.scrollTop = messageArea.scrollHeight;
            
            // Kirim ke backend
            try {{
                const response = await fetch(`${{API_URL}}/chat/${{companySlug}}`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ message: message, thread_id: threadId }})
                }});
                if (!response.ok) throw new Error('Failed to fetch response');
                const data = await response.json();
                
                // Hapus typing indicator
                messageArea.removeChild(typingDiv);
                
                // Tampilkan respons bot
                addMessage(data.response);
            }} catch (error) {{
                console.error('Error sending message:', error);
                messageArea.removeChild(typingDiv);
                addMessage('Maaf, terjadi kesalahan. Silakan coba lagi.', false);
            }}
        }};
        
        // Event listener untuk Enter
        input.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter' && !e.shiftKey) {{
                e.preventDefault();
                sendMessage();
            }}
        }});
        sendBtn.addEventListener('click', sendMessage);
        
        // Sesuaikan tinggi textarea secara dinamis
        input.addEventListener('input', () => {{
            input.style.height = '40px';
            input.style.height = `${{Math.min(input.scrollHeight, 100)}}px`;
        }});
        
        // Tampilkan pesan sambutan
        addMessage(config.greetingMessage || 'Halo! Bagaimana saya bisa membantu Anda?');
        
    }} catch (error) {{
        console.error('Error loading chatbot:', error);
        const errorMsg = document.createElement('div');
        errorMsg.innerHTML = 'Gagal memuat chatbot';
        errorMsg.style.position = 'fixed';
        errorMsg.style.bottom = '20px';
        errorMsg.style.right = '20px';
        errorMsg.style.padding = '12px';
        errorMsg.style.backgroundColor = '#ff4444';
        errorMsg.style.color = '#fff';
        errorMsg.style.borderRadius = '8px';
        errorMsg.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
        document.body.appendChild(errorMsg);
    }}
}})();
"""
    return PlainTextResponse(js_content, media_type="application/javascript")

    
    
@router.post("/chat/{company_slug}", response_model=dict)
async def handle_chat_message(company_slug: str, request: ChatRequest, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    try:
        conversation = db.query(Conversation).filter(Conversation.thread_id == request.thread_id).first()
        
        if not conversation:
            conversation = Conversation(
                thread_id=request.thread_id,
                company_id=company.id
            )
            db.add(conversation)
            db.commit() 
            db.refresh(conversation)

        user_message = Message(
            content=request.message,
            sender=MessageSender.USER,
            conversation_id=conversation.id
        )
        db.add(user_message)
        
        response_text = await process_chat_message_langgraph(
            company_id=company.id, 
            message=request.message,
            thread_id=request.thread_id
        )

        bot_message = Message(
            content=response_text,
            sender=MessageSender.BOT,
            conversation_id=conversation.id
        )
        db.add(bot_message)
        
        db.commit()
                
        return {"response": response_text}
        
    except Exception as e:
        print(f"Error processing chat message: {e}")
        db.rollback()
        return {"response": "Maaf, terjadi kesalahan dalam memproses pesan Anda. Silakan coba lagi."}
