from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.url_company import UrlCompanyCreate, UrlCompany, UrlCompanyCreateRequest
from app.models.url_company import UrlCompany as UrlCompanyModel
from app.models.company import Company
from app.config.database import get_db
from app.api.deps import get_current_user  
from app.models.user import User

router = APIRouter()

@router.post("/{slug}/urls", response_model=list[UrlCompany])
def create_urls_for_company(
    slug: str,
    urls_request: UrlCompanyCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = db.query(Company).filter(Company.slug == slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if company.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    created_urls = []
    for url in urls_request.urls:
        existing_url = db.query(UrlCompanyModel).filter(
            UrlCompanyModel.company_id == company.id,
            UrlCompanyModel.url == url
        ).first()
        
        if not existing_url:
            db_url = UrlCompanyModel(
                url=url,
                company_id=company.id
            )
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
            created_urls.append(db_url)

    return created_urls


@router.get("/{slug}/urls", response_model=list[UrlCompany])
def get_urls_for_company(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = db.query(Company).filter(Company.slug == slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if company.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    urls = db.query(UrlCompanyModel).filter(UrlCompanyModel.company_id == company.id).all()

    return urls

@router.delete("/{slug}/urls/{url_id}")
def delete_url_for_company(
    slug: str,
    url_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = db.query(Company).filter(Company.slug == slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if company.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    url = db.query(UrlCompanyModel).filter(
        UrlCompanyModel.id == url_id,
        UrlCompanyModel.company_id == company.id
    ).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    db.delete(url)
    db.commit()

    return {"message": "URL deleted successfully"}