import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.company import CompanyCreate, CompanyResponse
from app.models.company import Company
from app.api.deps import get_current_user
from app.models.user import User
from app.utils.slugify import slugify

router = APIRouter(tags=["companies"])

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    company_in: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  
    ):
    unique_slug = str(uuid.uuid4())
    
    company = Company(name=company_in.name, slug=unique_slug, user_id=current_user.id)
    db.add(company)
    db.commit()
    db.refresh(company)

    return company

@router.get("/", response_model=list[CompanyResponse])
def get_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  
):
    companies = db.query(Company).filter(Company.user_id == current_user.id).all()
    return companies

@router.get("/{slug}", response_model=CompanyResponse)
def get_company_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  
):
    company = db.query(Company).filter(Company.slug == slug, Company.user_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company