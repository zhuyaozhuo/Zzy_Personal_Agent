import json
from datetime import datetime
from typing import Any


def json_serializer(obj: Any) -> str:
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def load_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: dict, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=json_serializer)
