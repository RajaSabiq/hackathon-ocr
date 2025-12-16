from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class JobStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class BoundingBox(BaseModel):
    text: str
    confidence: float
    bbox: List[int]  # [x, y, width, height]

class OCRResult(BaseModel):
    filename: str
    text: str
    confidence: float
    language: str
    bbox_data: List[BoundingBox]
    page_number: Optional[int] = None

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    files_count: int

class ResultResponse(BaseModel):
    job_id: str
    status: JobStatus
    results: List[OCRResult]
    error_message: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    tesseract_version: str