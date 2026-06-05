from pydantic import BaseModel
from typing import Literal


class ProcessedFile(BaseModel):
    original_name: str
    new_name: str
    doc_type: str
    doc_type_display: str
    folder: str
    pages: int
    was_ocr: bool
    confidence: Literal["high", "medium", "low"]
    error: str | None = None


class MissingDoc(BaseModel):
    key: str
    display: str


class ProcessingStats(BaseModel):
    total_uploaded: int
    total_output: int
    splits_performed: int
    ocr_applied: int


class ProcessingResult(BaseModel):
    files: list[ProcessedFile]
    missing_docs: list[MissingDoc]
    download_token: str
    stats: ProcessingStats
