from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
import tempfile
from app.storage.memory import save_result, get_result
from app.tasks.ocr_task import run_ocr_task
from app.models import OCRJobResponse, OCRProcessingResponse, OCRCompletedResponse

app = FastAPI(title="PDF OCR Extractor", version="1.0.0")

# Health check
@app.get("/")
def health_check():
    return {"status": "ok"}

# POST: upload PDF
@app.post("/extract", response_model=OCRJobResponse)
async def extract_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    # save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        pdf_path = tmp.name

    result_id = save_result({"status": "processing"})
    background_tasks.add_task(run_ocr_task, result_id, pdf_path)

    return OCRJobResponse(id=result_id, status="processing")

# GET: retrieve result
@app.get("/result/{result_id}")
def get_extraction_result(result_id: str):
    result = get_result(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    if result["status"] == "processing":
        return OCRProcessingResponse(id=result_id, status="processing")

    return OCRCompletedResponse(
        id=result_id,
        status="completed",
        full_text=result.get("full_text"),
        duration_seconds=result.get("duration_seconds")
    )
