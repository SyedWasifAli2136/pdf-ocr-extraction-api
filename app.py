from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from crop_pdf_files import crop_multiple_pdfs
from ocr_engine import process_files_in_directory, save_extracted_texts

app = FastAPI()

# Directories
INPUT_PDF_DIR = "sample_pdfs"
CROPPED_PDF_DIR = "output_pdfs"
EXTRACTED_TEXT_DIR = "extracted_texts"
EXTRACTED_TEXT_JSON = "extracted_texts.json"

# Ensure directories exist
os.makedirs(INPUT_PDF_DIR, exist_ok=True)
os.makedirs(CROPPED_PDF_DIR, exist_ok=True)
os.makedirs(EXTRACTED_TEXT_DIR, exist_ok=True)


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file for processing."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = os.path.join(INPUT_PDF_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": f"File {file.filename} uploaded successfully."}


@app.post("/crop-pdfs/")
def crop_pdfs():
    """Crop all uploaded PDFs."""
    if not os.listdir(INPUT_PDF_DIR):
        raise HTTPException(status_code=400, detail="No PDF files to crop.")

    crop_multiple_pdfs(INPUT_PDF_DIR, CROPPED_PDF_DIR)
    return {"message": "All PDFs cropped successfully.", "output_directory": CROPPED_PDF_DIR}


@app.post("/extract-text/")
def extract_text():
    """Extract text from all cropped PDFs."""
    if not os.listdir(CROPPED_PDF_DIR):
        raise HTTPException(status_code=400, detail="No cropped PDFs to extract text from.")

    extracted_texts = process_files_in_directory(CROPPED_PDF_DIR, EXTRACTED_TEXT_DIR)
    save_extracted_texts(extracted_texts, EXTRACTED_TEXT_JSON)

    return {
        "message": "Text extracted successfully.",
        "output_directory": EXTRACTED_TEXT_DIR,
        "json_file": EXTRACTED_TEXT_JSON,
    }
