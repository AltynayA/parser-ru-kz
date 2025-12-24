import os
import time
import logging
from app.storage.memory import update_result
from app.ocr.pdf_converter import pdf_to_images
from app.ocr.ocr_engine import image_to_text
from app.ocr.text_utils import extract_text_after_heading

from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OCR")
BASE_STORAGE = Path("/storage/logs")
RESULT_JSON_DIR = BASE_STORAGE / "json"
RESULT_TEXT_DIR = BASE_STORAGE / "texts"

RESULT_JSON_DIR.mkdir(parents=True, exist_ok=True)
RESULT_TEXT_DIR.mkdir(parents=True, exist_ok=True)


def run_ocr_task(result_id: str, pdf_path: str, heading: str | None):
    start_time = time.time()
    try:
        images = pdf_to_images(pdf_path)
        full_text = ""

        for idx, img in enumerate(images):
            logger.info(f"[OCR] Processing page {idx+1}/{len(images)}")
            page_text = image_to_text(img)
            # text = image_to_text(img)
            full_text += page_text + "\n"

            if heading and not extracted_text:
                if heading.lower().strip() in page_text.lower():
                    extracted_text = extract_text_after_heading(page_text, heading)

        if not heading:
            extracted_text = full_text

        duration = time.time() - start_time

        # Update result in memory
        update_result(result_id, 
                    {
                        "status": "completed",
                        "heading": heading,
                        "full_text": full_text.strip(),
                        "extracted_text": extracted_text.strip(),
                        "duration_seconds": round(duration, 3)
                    }
        )
        # save json
        json_path = RESULT_JSON_DIR / f"{result_id}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "result_id": result_id,
                # "status": "completed",
                "heading": heading,
                "full_text": full_text.strip(),
                "extracted_text": extracted_text.strip(),
                "duration_seconds": round(duration, 3)
            }, f, ensure_ascii=False, indent=2)
            
        text_path = RESULT_TEXT_DIR / f"{result_id}.txt"
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(extracted_text.strip())

            # for full text
        full_text_path = RESULT_TEXT_DIR / f"{result_id}_full.txt"
        with open(full_text_path, "w", encoding="utf-8") as f:
            f.write(full_text.strip())

        logger.info(
            f"[OCR] Completed {result_id} in {round(duration, 3)}s | "
            f"heading={'YES' if heading else 'NO'}"
        )
        # logger.info(f"[OCR] Completed for result_id={result_id} in {round(duration, 3)}s")

    except Exception as e:
        logger.error(f"[OCR] Failed for result_id={result_id}: {e}", exc_info=True)
        update_result(result_id, {
            "status": "failed",
            "full_text": "",
            "extracted_text": "",
            "error": str(e)
        })

    finally:
        # cleanup temp PDF
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception as e:
                logger.warning(f"Failed to remove temp PDF {pdf_path}: {e}")
