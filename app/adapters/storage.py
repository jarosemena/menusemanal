import json
from pathlib import Path
from typing import List, Dict


def load_data(file_name: str) -> List[Dict]:
    path = Path("data\\json\\") / file_name
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list) and "data" in data[0]:
        return data[0]["data"]
    return data
