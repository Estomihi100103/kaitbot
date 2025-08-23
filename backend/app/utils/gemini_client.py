import os
import logging
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

# Init Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_embeddings(texts: List[str], model: str | None = None, output_dim: int = 1536) -> List[List[float]]:
    """
    Generate embeddings for a list of texts synchronously using Google Gemini.
    """
    model = model or os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")
    result = client.models.embed_content(
        model=model,
        contents=texts,
        config=types.EmbedContentConfig(
            output_dimensionality=output_dim,
            task_type="SEMANTIC_SIMILARITY"
        )
    )
    return [e.values for e in result.embeddings]

def generate_keywords(text: str, model: str = None) -> str:
    """
    Generate keywords from a given text using Google Gemini.
    """
    model = model or os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")
    prompt = (
        "You are an expert in information retrieval.Based on the following text, generate 10 keywords search that best represent its content.Select only terms or phrases that are most relevant and useful. Do not include any other text or explanation. Just return the keywords. Here is the text: \n\n"
        f"{text}"
    )

    result = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return result.text


