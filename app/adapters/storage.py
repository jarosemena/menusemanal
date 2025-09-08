import json
from pathlib import Path
from typing import List, Dict, Any, Union


def load_data(file_name: str) -> List[Dict[str, Any]]:
    path = Path("data\\json\\") / file_name
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Manejar el caso de lista vacía
    if isinstance(data, list) and len(data) == 0:
        return []
    
    # Manejar la estructura anidada con clave "data"
    if (isinstance(data, list) and 
        len(data) > 0 and 
        isinstance(data[0], dict) and 
        "data" in data[0]):
        return data[0]["data"]
    
    # Para listas simples o otros formatos
    return data