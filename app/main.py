from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
import tempfile
from app.storage.memory import save_result, get_result
from app.tasks.ocr_task import run_ocr_task
from app.models import OCRJobResponse, OCRProcessingResponse, OCRCompletedResponse

app = FastAPI(title="PDF OCR Extractor", version="1.0.0")

# health check
@app.get("/")
def health_check():
    return {"status": "ok"}

# POST: upload PDF
@app.post("/extract", response_model=OCRJobResponse)
async def extract_pdf(
    file: UploadFile = File(...), 
    heading: str = "",  
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    # save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        pdf_path = tmp.name

    result_id = save_result({"heading": heading, "status": "processing"})

    background_tasks.add_task(
        run_ocr_task,
        result_id,
        pdf_path,
        heading if heading else None
    )

    return OCRJobResponse(id=result_id, status="processing")

# GET: retrieve result
@app.get("/result/{result_id}", response_model=OCRCompletedResponse | OCRProcessingResponse)
def get_extraction_result(result_id: str):
    result = get_result(result_id)

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    if result["status"] == "processing":
        return OCRProcessingResponse(id=result_id, status="processing")

    return OCRCompletedResponse(
        id=result_id,
        status="completed",
        heading=result.get("heading"),
        # full_text=result.get("full_text"),
        extracted_text=result.get("extracted_text"),
        duration_seconds=result.get("duration_seconds", 0)
    )
