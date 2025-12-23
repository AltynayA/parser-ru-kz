import uuid

# Simple in-memory storage
STORAGE = {}

def save_result(data: dict) -> str:
    result_id = str(uuid.uuid4())
    STORAGE[result_id] = data
    return result_id

def get_result(result_id: str) -> dict | None:
    return STORAGE.get(result_id)

def update_result(result_id: str, data: dict):
    if result_id in STORAGE:
        STORAGE[result_id].update(data)
