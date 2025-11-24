import os
import aiofiles
from fastapi import UploadFile, HTTPException
from typing import List, Optional
from bs4 import BeautifulSoup
import fitz  # PyMuPDF for PDF parsing
import json

async def save_uploaded_file(upload_file: UploadFile, storage_dir: str) -> str:
    """
    Save an uploaded file asynchronously to the given storage directory.
    Ensures the directory exists, and saves with a safe unique filename.
    Returns the absolute path to the saved file.
    """
    os.makedirs(storage_dir, exist_ok=True)

    filename = upload_file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename.")

    # Simple filename sanitization (avoid spaces/special chars)
    safe_filename = filename.replace(" ", "_")
    file_path = os.path.join(storage_dir, safe_filename)
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await upload_file.read()
            if not content:
                raise HTTPException(status_code=400, detail=f"File {filename} is empty.")
            await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file {filename}: {str(e)}")
    finally:
        await upload_file.close()
    return file_path

async def parse_pdf(file_path: str) -> str:
    """
    Extracts text from all pages of the PDF file.
    Raises HTTPException if unable to open or read file content.
    """
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open PDF: {str(e)}")

    texts = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        if text:
            texts.append(text)
    if not texts:
        raise HTTPException(status_code=400, detail="No text found in PDF document.")

    return "\n".join(texts)

async def parse_json(file_path: str) -> str:
    """
    Read JSON file asynchronously and serialize to readable string for embedding.
    Raises HTTPException on parsing errors.
    """
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            data = await f.read()
        json_obj = json.loads(data)
        # Convert JSON to pretty string with indentation
        json_str = json.dumps(json_obj, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading JSON file: {str(e)}")

    return json_str

async def parse_html(file_path: str) -> str:
    """
    Parses an HTML file and extracts visible text content with minimal formatting.
    Raises HTTPException if file cannot be read.
    """
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            html_content = await f.read()
        if not html_content.strip():
            raise HTTPException(status_code=400, detail="HTML file is empty.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read HTML file: {str(e)}")

    soup = BeautifulSoup(html_content, "html.parser")

    # Remove scripts and styles
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Get visible text
    text = soup.get_text(separator="\n")

    # Clean and normalize text
    lines = (line.strip() for line in text.splitlines())
    clean_text = "\n".join(line for line in lines if line)

    if not clean_text.strip():
        raise HTTPException(status_code=400, detail="No visible text found in HTML document.")

    return clean_text
