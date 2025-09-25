# test_almuerzos.py
import json
from pathlib import Path
import pytest
from app.adapters.storage import load_data


def test_load_almuerzos_nested_structure(tmp_path, monkeypatch):
    """Prueba cargar almuerzos.json con estructura anidada [{'data': [...]}]"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)
    
    file_path = data_dir / "almuerzos.json"
    
    # Estructura anidada (como el archivo real espera)
    almuerzos_data = [
        {
            "data": [
                {
                    "id": 1,
                    "Proteina": "Pollo",
                    "Complemento": " con Arroz blanco y Ensalada de papa",
                    "Descripcion": "Pollo a la Reina con Arroz blanco y Ensalada de papa",
                    "RecetaCode": None,
                    "SuperListCode": None,
                    "TipoCocionProteina": "a la Reina"
                }
            ]
        }
    ]
    
    file_path.write_text(json.dumps(almuerzos_data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    
    result = load_data("almuerzos.json")
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["Proteina"] == "Pollo"


def test_load_almuerzos_direct_dict_structure(tmp_path, monkeypatch):
    """Prueba almuerzos.json con estructura de diccionario directo {'data': [...]}"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)
    
    file_path = data_dir / "almuerzos.json"
    
    # Estructura de diccionario directo (ahora debería funcionar)
    dict_data = {
        "data": [
            {
                "id": 1,
                "Proteina": "Pollo",
                "Complemento": " con Arroz blanco",
                "Descripcion": "Pollo a la Reina con Arroz blanco",
                "TipoCocionProteina": "a la Reina"
            }
        ]
    }
    
    file_path.write_text(json.dumps(dict_data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    
    result = load_data("almuerzos.json")
    
    # Ahora debería devolver la lista, no el diccionario completo
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["Proteina"] == "Pollo"


def test_load_almuerzos_simple_list_structure(tmp_path, monkeypatch):
    """Prueba almuerzos.json con estructura de lista simple"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)
    
    file_path = data_dir / "almuerzos.json"
    
    # Estructura de lista simple (sin anidación)
    simple_data = [
        {
            "id": 1,
            "Proteina": "Pollo",
            "Complemento": " con Arroz blanco",
            "Descripcion": "Pollo a la Reina con Arroz blanco",
            "TipoCocionProteina": "a la Reina"
        }
    ]
    
    file_path.write_text(json.dumps(simple_data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    
    result = load_data("almuerzos.json")
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["Proteina"] == "Pollo"


def test_load_almuerzos_empty_structures(tmp_path, monkeypatch):
    """Prueba varias estructuras vacías"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)
    monkeypatch.chdir(tmp_path)
    
    # Lista vacía simple
    file_path = data_dir / "empty1.json"
    file_path.write_text("[]", encoding="utf-8")
    result = load_data("empty1.json")
    assert isinstance(result, list)
    assert len(result) == 0
    
    # Lista con diccionario vacío
    file_path = data_dir / "empty2.json"
    file_path.write_text('[{"data": []}]', encoding="utf-8")
    result = load_data("empty2.json")
    assert isinstance(result, list)
    assert len(result) == 0
    
    # Diccionario con lista vacía
    file_path = data_dir / "empty3.json"
    file_path.write_text('{"data": []}', encoding="utf-8")
    result = load_data("empty3.json")
    assert isinstance(result, list)
    assert len(result) == 0


def test_load_almuerzos_different_proteins(tmp_path, monkeypatch):
    """Prueba diferentes tipos de proteínas"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)
    
    file_path = data_dir / "almuerzos.json"
    
    almuerzos_data = {
        "data": [
            {
                "id": 1,
                "Proteina": "Pollo",
                "Complemento": " con Arroz blanco",
                "Descripcion": "Pollo a la Reina con Arroz blanco",
                "TipoCocionProteina": "a la Reina"
            },
            {
                "id": 727,
                "Proteina": "Carne de Res",
                "Complemento": " con Arroz con lentejas",
                "Descripcion": "Carne de Res Bolitas al Vino con Arroz con lentejas",
                "TipoCocionProteina": "Bolitas al Vino"
            },
            {
                "id": 807,
                "Proteina": "Pescado",
                "Complemento": " con Arroz con lentejas y Ensalada de papa",
                "Descripcion": "Pescado Frito con Arroz con lentejas y Ensalada de papa",
                "TipoCocionProteina": "Frito"
            }
        ]
    }
    
    file_path.write_text(json.dumps(almuerzos_data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    
    result = load_data("almuerzos.json")
    
    assert len(result) == 3
    proteins = [item["Proteina"] for item in result]
    assert "Pollo" in proteins
    assert "Carne de Res" in proteins
    assert "Pescado" in proteins


def test_load_almuerzos_null_values(tmp_path, monkeypatch):
    """Prueba manejo de valores nulos"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)
    
    file_path = data_dir / "almuerzos.json"
    
    almuerzos_data = {
        "data": [
            {
                "id": 865,
                "Proteina": "Mixto",
                "Complemento": " con arroz Blanco",
                "Descripcion": "Mixto con arroz Blanco",
                "RecetaCode": None,
                "SuperListCode": None,
                "TipoCocionProteina": None
            }
        ]
    }
    
    file_path.write_text(json.dumps(almuerzos_data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    
    result = load_data("almuerzos.json")
    
    assert result[0]["RecetaCode"] is None
    assert result[0]["SuperListCode"] is None
    assert result[0]["TipoCocionProteina"] is None