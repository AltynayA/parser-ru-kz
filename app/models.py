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
    # full_text: str
    heading: Optional[str]
    heading: str | None = None
    duration_seconds: float
