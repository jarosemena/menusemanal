# storage.py
import json
from pathlib import Path
from typing import List, Dict, Any


def load_data(file_name: str) -> List[Dict[str, Any]]:
    path = Path("data") / "json" / file_name
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Manejar el caso de lista vacía
    if isinstance(data, list) and len(data) == 0:
        return []
    
    # Manejar la estructura anidada con clave "data" en una lista
    if (isinstance(data, list) and 
        len(data) > 0 and 
        isinstance(data[0], dict) and 
        "data" in data[0]):
        return data[0]["data"]
    
    # Manejar la estructura de diccionario directo con clave "data"
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    
    # Para listas simples u otros formatos
     # Limpiar espacios en los datos
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, str):
                        item[key] = value.strip()
                        
    return data