import docx
import logging
import pdfplumber
from langchain_community.document_loaders  import TextLoader

logger = logging.getLogger(__name__)

def _load_text_from_pdf(path: str) -> str:
    try:
        with pdfplumber.open(path) as pdf:
            full_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)
            return '\n'.join(full_text).strip()
    except Exception as e:
        logger.error(f"Error loading PDF file {path}: {e}")
        return ""

def _load_text_from_docx(path: str) -> str:
    try:
        doc = docx.Document(path)
        return '\n'.join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        logger.error(f"Error loading DOCX file {path}: {e}")
        return ""
    
def _load_text_from_md(path:str)->str:
    try:
        loader = TextLoader(path, encoding='utf-8')
        return loader.load()[0].page_content.strip()
    except Exception as e:
        logger.error(f"Error loading Markdown file {path}: {e}")
        return ""