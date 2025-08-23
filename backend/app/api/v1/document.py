from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.company import Company
from app.schemas.document import DocumentCreateResponse
from app.repositories.document_repository import create_document_record
from app.services.document_service import process_document

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=DocumentCreateResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    title: str = Form(...),
    company_slug: str = Form(...),
    folder_id: int | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = db.query(Company).filter(Company.slug == company_slug, Company.user_id == current_user.id).first()
    
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    file_bytes = file.file.read()

    doc = create_document_record(
        db=db,
        title=title,
        file_type=(file.filename.split('.')[-1] if '.' in file.filename else 'bin'),
        file_path=None,
        company_id=company.id,
        folder_id=folder_id,
        keywords_search=None,
        status='processing',
    )

    drivername = db.get_bind().dialect.name

    process_document(
        document_id=doc.id,
        company_id=company.id,
        original_filename=file.filename,
        file_bytes=file_bytes,
        company_slug=company.slug,
        db_drivername=drivername,
    )

    return DocumentCreateResponse.from_orm(doc)

