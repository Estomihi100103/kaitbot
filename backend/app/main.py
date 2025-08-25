import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.auth import router as auth_router
from app.api.v1.folder import router as folder_router
from app.api.v1.company import router as company_router
from app.api.v1.document import router as document_router
from app.api.v1.chatbot_endpoints import router as chatbot_router
from app.api.v1.url_company import router as url_company_router
from app.api.v1.conversation import router as conversation_router
from app.middleware.cors import add_cors_middleware

app = FastAPI(title="My App API", version="1.0.0")
# static_dir = os.path.join(os.path.dirname(__file__), "static")
# app.mount("/static", StaticFiles(directory=static_dir), name="static")

add_cors_middleware(app)

app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(company_router, prefix="/api/v1/companies")
app.include_router(folder_router, prefix="/api/v1/companies")
app.include_router(document_router, prefix="/api/v1")
app.include_router(chatbot_router, prefix="/api/v1/chatbot")
app.include_router(url_company_router, prefix="/api/v1/companies")
app.include_router(conversation_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to My App API"}