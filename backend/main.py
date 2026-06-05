import os
import uuid
import tempfile
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from models import ProcessingResult, ProcessedFile, MissingDoc, ProcessingStats
from classifier import classify_document, get_missing_docs, get_folder, get_display_name, DOC_TYPES
from pdf_processor import extract_text, needs_ocr, ocr_pdf, split_pdf, convert_image_to_pdf, get_page_count
from packager import build_zip

app = FastAPI(title="TC Doc Tool")

# In production (Railway) the frontend is served from the same origin — no CORS needed.
# In development the Vite dev server runs on a different port, so allow localhost.
_IS_PROD = bool(os.environ.get("RAILWAY_ENVIRONMENT"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if _IS_PROD else ["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store: token -> zip path
_zip_store: dict[str, str] = {}

SUPPORTED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".tif", ".docx", ".xlsx"}


@app.post("/api/process", response_model=ProcessingResult)
async def process_files(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    work_dir = tempfile.mkdtemp(prefix="tc_")
    uploads_dir = os.path.join(work_dir, "uploads")
    split_dir = os.path.join(work_dir, "split")
    output_dir = os.path.join(work_dir, "output")
    os.makedirs(uploads_dir)
    os.makedirs(split_dir)
    os.makedirs(output_dir)

    try:
        # Save uploaded files
        saved = []
        for upload in files:
            ext = Path(upload.filename).suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            dest = os.path.join(uploads_dir, upload.filename)
            with open(dest, "wb") as f:
                f.write(await upload.read())
            saved.append((upload.filename, dest, ext))

        if not saved:
            raise HTTPException(status_code=400, detail="No supported files found.")

        # Process each file — failures are isolated per file, never abort the batch
        to_classify: list[tuple[str, str, int, bool, str | None]] = []  # (original_name, path, pages, was_ocr, error)
        splits_performed = 0
        ocr_applied = 0

        for original_name, file_path, ext in saved:
            try:
                if ext in {".jpg", ".jpeg", ".png", ".tiff", ".tif"}:
                    pdf_path = os.path.join(split_dir, Path(original_name).stem + ".pdf")
                    convert_image_to_pdf(file_path, pdf_path)
                    to_classify.append((original_name, pdf_path, 1, True, None))
                    ocr_applied += 1

                elif ext == ".pdf":
                    working_path = file_path
                    was_ocr = False
                    try:
                        if needs_ocr(file_path):
                            ocr_path = os.path.join(split_dir, "ocr_" + Path(original_name).name)
                            ocr_pdf(file_path, ocr_path)
                            working_path = ocr_path
                            was_ocr = True
                            ocr_applied += 1
                    except Exception:
                        # OCR failed — continue with original (text-layer extraction will still work)
                        working_path = file_path

                    try:
                        parts = split_pdf(working_path, split_dir)
                    except Exception:
                        parts = [working_path]

                    if len(parts) > 1:
                        splits_performed += len(parts) - 1
                        for i, part in enumerate(parts):
                            part_name = f"{Path(original_name).stem}_part{i+1}.pdf"
                            to_classify.append((part_name, part, get_page_count(part), was_ocr, None))
                    else:
                        to_classify.append((original_name, working_path, get_page_count(working_path), was_ocr, None))

                elif ext in {".docx", ".xlsx"}:
                    to_classify.append((original_name, file_path, 1, False, None))

            except Exception as exc:
                # File could not be processed at all — copy as-is to Misc
                dest_folder = os.path.join(output_dir, "07_Misc")
                os.makedirs(dest_folder, exist_ok=True)
                shutil.copy2(file_path, os.path.join(dest_folder, original_name))
                to_classify.append((original_name, file_path, 1, False, str(exc)))

        # Classify and rename
        processed_files: list[ProcessedFile] = []
        type_counter: dict[str, int] = {}
        found_types: list[str] = []

        for original_name, file_path, pages, was_ocr, file_error in to_classify:
            try:
                text = extract_text(file_path) if not file_error else ""
                doc_type = classify_document(original_name, text)
                confidence = _confidence(doc_type, original_name, text)
            except Exception:
                text, doc_type, confidence = "", "Unknown", "low"

            type_counter[doc_type] = type_counter.get(doc_type, 0) + 1
            count = type_counter[doc_type]
            suffix = f"_{count}" if count > 1 else ""
            ext = Path(file_path).suffix
            new_name = f"{doc_type}{suffix}{ext}"

            folder = get_folder(doc_type)

            if not file_error:
                # File not yet copied — place it now
                dest_folder = os.path.join(output_dir, folder)
                os.makedirs(dest_folder, exist_ok=True)
                try:
                    shutil.copy2(file_path, os.path.join(dest_folder, new_name))
                except Exception as exc:
                    file_error = str(exc)

            processed_files.append(ProcessedFile(
                original_name=original_name,
                new_name=new_name,
                doc_type=doc_type,
                doc_type_display=get_display_name(doc_type),
                folder=folder,
                pages=pages,
                was_ocr=was_ocr,
                confidence=confidence,
                error=file_error,
            ))

            if doc_type != "Unknown":
                found_types.append(doc_type)

        # Missing docs
        missing_docs = [MissingDoc(key=d["key"], display=d["display"]) for d in get_missing_docs(found_types)]

        # Build ZIP
        token = str(uuid.uuid4())
        zip_path = os.path.join(work_dir, f"transaction_{token}.zip")
        build_zip(output_dir, zip_path, missing_docs)
        _zip_store[token] = zip_path

        return ProcessingResult(
            files=processed_files,
            missing_docs=missing_docs,
            download_token=token,
            stats=ProcessingStats(
                total_uploaded=len(saved),
                total_output=len(processed_files),
                splits_performed=splits_performed,
                ocr_applied=ocr_applied,
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        shutil.rmtree(work_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{token}")
def download_zip(token: str):
    zip_path = _zip_store.get(token)
    if not zip_path or not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="File not found or expired.")
    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="transaction_files.zip",
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}


# ── Serve React build (production) ──────────────────────────────────────────
# Must come AFTER all /api routes so FastAPI handles those first.
_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(_DIST):
    app.mount("/", StaticFiles(directory=_DIST, html=True), name="frontend")


def _confidence(doc_type: str, filename: str, text: str) -> str:
    if doc_type == "Unknown":
        return "low"
    filename_lower = filename.lower()
    config = DOC_TYPES.get(doc_type, {})
    for pattern in config.get("filename_patterns", []):
        if pattern.lower() in filename_lower:
            return "high"
    text_lower = text.lower()[:1000]
    for kw in config.get("keywords", []):
        if kw.lower() in text_lower[:300]:
            return "high"
    return "medium"
