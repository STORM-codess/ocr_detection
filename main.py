# main.py
import os
import shutil
import tempfile
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ocr.extract import extract_clean_lines
from ocr.parser import extract_structured_fields
from ocr.compare import compare_and_score

app = FastAPI(title="Document Verifier API")

# Allow CORS from anywhere or restrict to your friend's domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to ["https://your-frontend.com"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXT = {"png", "jpg", "jpeg"}

def save_upload_tmp(upload_file: UploadFile) -> str:
    suffix = os.path.splitext(upload_file.filename)[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        tmp.write(upload_file.file.read())
        tmp.flush()
    finally:
        tmp.close()
    return tmp.name

@app.post("/verify-document")
async def verify_document(
    name: str = Form(...),
    dob: str = Form(...),
    address: str = Form(...),
    file: UploadFile = File(...)
):
    # basic validation
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # save temp file
    tmp_path = save_upload_tmp(file)

    try:
        # OCR (hidden)
        lines = extract_clean_lines(tmp_path)

        # parse
        doc_fields = extract_structured_fields(lines)

        # prepare user dict (normalize lowercase and strip)
        user = {
            "name": name.lower().strip(),
            "dob": dob.lower().strip(),
            "address": address.lower().strip()
        }

        # compare & score
        result = compare_and_score(user, doc_fields)

        # return full extracted fields too
        response = {
            "status": result["status"],
            "name_match": result["name_match"],
            "dob_match": result["dob_match"],
            "address_confidence": result["address_confidence"],
            "document_details": result["document_details"]
        }
        return JSONResponse(content=response)

    finally:
        # cleanup
        try:
            os.remove(tmp_path)
        except Exception:
            pass
