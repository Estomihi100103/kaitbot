import os
import json
import logging
from app.utils.storage import save_bytes_to_file
from app.utils.loaders import _load_text_from_pdf, _load_text_from_docx, _load_text_from_md
from app.utils.gemini_client import generate_embeddings, generate_keywords
from app.repositories.document_repository import update_document_file_and_keywords, bulk_create_embeddings
from app.config.database import SessionLocal
from app.services.chunking_service import generate_contextual_chunks, overlap_chunk_texts

logger = logging.getLogger(__name__)

def _load_text_from_file(path: str) -> str:
    ext=os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        texts = _load_text_from_pdf(path)
    elif ext in [".doc", ".docx"]:
        texts = _load_text_from_docx(path)
    elif ext =='.md': 
        texts = _load_text_from_md(path)
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        logger.warning(f"[Unsupported file extension: {ext}")
        return ""

    return '\n'.join(texts).strip()

def _preprocess_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n") 
    text = text.replace("```", "").replace("`", "")
    return text.lower()


def _chunk_texts(full_text: str) -> list:
    """
    Memecah teks menjadi chunk.
    Mencoba menggunakan chunking berbasis LLM, jika gagal akan fallback ke chunking tradisional.
    """
    try:
        json_string_chunks = generate_contextual_chunks(full_text)
        if not json_string_chunks:
            raise ValueError("LLM returned no chunks.")
        cleaned_json = json_string_chunks.strip().replace('```json', '').replace('```', '')
        list_of_dicts = json.loads(cleaned_json)
        
        chunks = [item['content'] for item in list_of_dicts if 'content' in item]
        
        if not chunks:
            raise ValueError("Parsed JSON contains no 'content' chunks.")
            
        return chunks
        
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        chunks = overlap_chunk_texts(full_text)
        return chunks
    except Exception as e:
        chunks = overlap_chunk_texts(full_text)
        return chunks

def process_document(document_id: int, company_id:int, original_filename: str, file_bytes: bytes, company_slug: str, db_drivername: str):
    db = None
    try:
        db = SessionLocal()
        # 1. Save file
        saved_path = save_bytes_to_file(file_bytes, original_filename, company_slug)
        
        # 2. Load text
        full_text = _load_text_from_file(saved_path)
        
        # 3. Preprocess
        preprocessed = _preprocess_text(full_text)
        
        # # 4. Generate keywords
        # keywords = generate_keywords(preprocessed)
        
        # 5. Chunking
        chunks = _chunk_texts(preprocessed)
        
        # 6. Update document record dengan path dan keywords
        update_document_file_and_keywords(db, document_id, saved_path, keywords=None)
        
        # 7. Generate embeddings in batches
        total_chunks = len(chunks)
        vectors = []
        batch_size = 16
        total_batches = (total_chunks + batch_size - 1) // batch_size

        for batch_index in range(total_batches):
            start_idx = batch_index * batch_size
            end_idx = min(start_idx + batch_size, total_chunks)
            batch = chunks[start_idx:end_idx]
            vecs = generate_embeddings(batch)

            for chunk_text, vec in zip(batch, vecs):
                vectors.append({
                    "chunk_content": chunk_text,
                    "embedding": vec
                })
        
        # 8. Simpan embeddings ke DB
        bulk_create_embeddings(db, document_id, company_id, vectors)

    except Exception as e:
        logger.exception(f"[Doc:{document_id}] Error: {e}")
    finally:
        if db:
            db.close()
            logger.info(f"[Doc:{document_id}] Database session closed.")