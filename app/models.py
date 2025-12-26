from pydantic import BaseModel
from typing import Optional

class OCRResponse(BaseModel):
    id: str
    status: str
    heading: Optional[str] = None
    extracted_text: Optional[str] = None
    duration_seconds: Optional[float] = None
    full_text: Optional[str] = None

