# PDF OCR Extraction API

A production-ready FastAPI service that automates **PDF cropping** and **text extraction** using PaddleOCR. Upload PDFs, crop to region of interest, and extract structured text — all via REST API endpoints.

---

## Features

- **PDF Upload** — Accept and store PDFs via REST API
- **Smart Cropping** — Crop PDFs to specific regions based on filename prefix rules (`sample_*`, `dual_*`)
- **OCR Extraction** — Extract text from cropped PDFs and images using PaddleOCR (angle-correction enabled)
- **Batch Processing** — Process entire directories of PDFs in one call
- **Structured Output** — Save extracted text as individual `.txt` files and a combined `extracted_texts.json`
- **Multi-format Support** — Handles PDF, PNG, JPG, JPEG inputs

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI + Uvicorn |
| OCR Engine | PaddleOCR |
| PDF Processing | PyMuPDF (fitz), pdf2image |
| Image Handling | Pillow |
| Output Format | JSON + TXT |

---

## Project Structure

```
pdf-ocr-extraction-api/
│
│
├── app.py                  # FastAPI app — all API endpoints
├── crop_pdf.py             # Single PDF cropping logic (PyMuPDF)
├── crop_pdf_files.py       # Batch PDF cropping with prefix-based rules
├── ocr_engine.py           # PaddleOCR text extraction (PDF + image)
│
├── sample_pdfs/                # Upload directory for input PDFs
├── output_pdfs/                # Cropped PDFs output directory
├── extracted_texts/            # Per-file extracted .txt outputs
│
├── requirements.txt            # Python dependencies
├── .gitignore                  # Ignored files
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SyedWasifAli2136/pdf-ocr-extraction-api.git
cd pdf-ocr-extraction-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** PaddleOCR requires `paddlepaddle` to be installed separately. See [PaddleOCR installation guide](https://github.com/PaddlePaddle/PaddleOCR).

```bash
pip install paddlepaddle
```

> **Note:** `pdf2image` requires Poppler. Install it via:
> - **Ubuntu/Debian:** `sudo apt-get install poppler-utils`
> - **macOS:** `brew install poppler`
> - **Windows:** Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases)

### 4. Run the API server

```bash
cd src
uvicorn app:app --reload
```

API will be live at: `http://localhost:8000`

Interactive docs at: `http://localhost:8000/docs`

---

## API Endpoints

### `POST /upload-pdf/`
Upload a PDF file for processing.

**Request:** `multipart/form-data` with `file` field (PDF only)

**Response:**
```json
{
  "message": "File sample_1.pdf uploaded successfully."
}
```

---

### `POST /crop-pdfs/`
Crop all uploaded PDFs based on filename prefix rules.

| Prefix | Crop Area (x0, y0, x1, y1) |
|---|---|
| `sample_*` | `(0, 0, 500, 600)` |
| `dual_*` | `(0, 270, 600, 750)` |

**Response:**
```json
{
  "message": "All PDFs cropped successfully.",
  "output_directory": "output_pdfs"
}
```

---

### `POST /extract-text/`
Run OCR on all cropped PDFs and save extracted text.

**Response:**
```json
{
  "message": "Text extracted successfully.",
  "output_directory": "extracted_texts",
  "json_file": "extracted_texts.json"
}
```

---

## Pipeline Flow

```
Upload PDF  ──▶  /upload-pdf/
                      │
                      ▼
              /crop-pdfs/  (prefix-based crop rules)
                      │
                      ▼
            /extract-text/  (PaddleOCR → .txt + .json)
```

---

## Output Example

`extracted_texts.json`:
```json
{
  "cropped_sample_1.pdf": "Page 1\nInvoice Number: 12345\nDate: 01/01/2024\n...",
  "cropped_dual_2.pdf": "Page 1\nPolicy Holder: John Doe\n..."
}
```

---

## Configuration

Crop rules are defined in `src/crop_pdf_files.py`. To add a new prefix:

```python
elif filename.startswith("your_prefix"):
    crop_area = (x0, y0, x1, y1)
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built by [Syed Wasif Ali](https://github.com/SyedWasifAli2136) · AI Engineer*
