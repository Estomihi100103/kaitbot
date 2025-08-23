from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.folder import FolderCreate, Folder as FolderSchema
from app.models.folder import Folder as FolderModel
from app.models.company import Company
from app.config.database import get_db
from app.api.deps import get_current_user  
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentCreateResponse

router = APIRouter()

@router.post("/{slug}/folders", response_model=FolderSchema)
def create_folder_for_company(
    slug: str,
    folder: FolderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  
):
    company = db.query(Company).filter(Company.slug == slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if company.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    db_folder = FolderModel(
        name=folder.name,
        company_id=company.id
    )
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder

from app.schemas.folder import FolderWithDocs

@router.get("/{slug}/folders", response_model=list[FolderWithDocs])
def get_folders_for_company(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = db.query(Company).filter(Company.slug == slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if company.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    folders = db.query(FolderModel).filter(FolderModel.company_id == company.id).all()

    result = []
    for folder in folders:
        docs = db.query(Document).filter(Document.folder_id == folder.id).all()
        result.append(FolderWithDocs(
            id=folder.id,
            name=folder.name,
            company_id=folder.company_id,
            created_at=folder.created_at,
            document_count=len(docs),
            documents=[DocumentCreateResponse.from_orm(doc) for doc in docs]
        ))

    return result