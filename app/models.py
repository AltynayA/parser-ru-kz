from pydantic import BaseModel
from typing import Optional

class OCRJobResponse(BaseModel):
    id: str
    status: str

class OCRProcessingResponse(BaseModel):
    id: str
    status: str

class OCRCompletedResponse(BaseModel):
    id: str
    status: str
    heading: Optional[str] = None
    full_text: str
    extracted_text: str
    duration_seconds: float

