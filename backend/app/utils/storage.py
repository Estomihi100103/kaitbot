import os
from pathlib import Path
from uuid import uuid4

STORAGE_ROOT = Path(os.getenv('STORAGE_ROOT', 'static/uploads'))
STORAGE_ROOT.mkdir(parents=True, exist_ok=True)


def save_bytes_to_file(file_bytes: bytes, filename: str, company_slug: str) -> str:
    company_dir = STORAGE_ROOT / company_slug
    company_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(filename).suffix
    dest_name = f"{uuid4().hex}{ext}"
    dest = company_dir / dest_name
    with dest.open('wb') as f:
        f.write(file_bytes)
    return str(dest)