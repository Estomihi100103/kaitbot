from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.doc_embedding import DocEmbedding
from typing import List
from datetime import datetime


def create_document_record(db: Session, *, title: str, file_type: str, file_path: str | None,
                           company_id: int, folder_id: int | None, keywords_search: str | None, status: str = 'processing') -> Document:
    doc = Document(
        title=title,
        file_type=file_type,
        file_path=file_path or '',
        keywords_search=keywords_search,
        company_id=company_id,
        folder_id=folder_id,
        created_at=datetime.utcnow(),
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def update_document_file_and_keywords(db: Session, document_id: int, file_path: str, keywords: str | None):
    doc = db.query(Document).get(document_id)
    if not doc:
        raise ValueError('Document not found')
    doc.file_path = file_path
    doc.keywords_search = keywords
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def bulk_create_embeddings(db: Session, document_id: int, company_id: int, embeddings_data: List[dict]):
    rows = []
    for item in embeddings_data:
        row = DocEmbedding(
            chunk_content=item['chunk_content'],
            embedding=item['embedding'],
            extractmetadata=item.get('extractmetadata'),
            document_id=document_id,
            company_id=company_id,
        )
        rows.append(row)
    db.add_all(rows)
    db.commit()
    return rows