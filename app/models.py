from pydantic import BaseModel

class OCRJobResponse(BaseModel):
    id: str
    status: str

class OCRProcessingResponse(BaseModel):
    id: str
    status: str

class OCRCompletedResponse(BaseModel):
    id: str
    status: str
    full_text: str
    duration_seconds: float
