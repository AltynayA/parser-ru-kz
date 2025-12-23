import os
import time
import logging
from app.storage.memory import update_result
from app.ocr.pdf_converter import pdf_to_images
from app.ocr.ocr_engine import image_to_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OCR")

def run_ocr_task(result_id: str, pdf_path: str):
    start_time = time.time()
    try:
        images = pdf_to_images(pdf_path)
        full_text = ""

        for idx, img in enumerate(images):
            text = image_to_text(img)
            full_text += text + "\n"

        duration = time.time() - start_time

        # Update result in memory
        update_result(result_id, {
            "status": "completed",
            "full_text": full_text.strip(),
            "duration_seconds": round(duration, 3)
        })

        logger.info(f"[OCR] Completed for result_id={result_id} in {round(duration, 3)}s")

    except Exception as e:
        logger.error(f"[OCR] Failed for result_id={result_id}: {e}", exc_info=True)
        update_result(result_id, {
            "status": "failed",
            "full_text": "",
            "error": str(e)
        })
