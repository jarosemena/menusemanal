# test_storage.py
import json
import pytest
from app.adapters.storage import load_data


def test_load_cenas_data_with_nested_structure(tmp_path, monkeypatch):
    """Prueba cargar datos de cenas.json que tienen estructura anidada"""
    # Crear directorio data/json
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)

    file_path = data_dir / "cenas.json"

    # Datos de ejemplo basados en la estructura real de cenas.json
    cenas_data = [
        {
            "data": [
                {
                    "id": 17,
                    "created_at": "2025-08-24T00:00:00+00:00",
                    "Proteina": "Huevo",
                    "Complemento": None,
                    "Descripcion": "Huevo Omelets jamon y queso",
                    "RecetaCode": None,
                    "SuperListCode": None,
                    "TipoCocionProteina": "Omelets jamon y queso"
                }
            ]
        }
    ]

    file_path.write_text(json.dumps(cenas_data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = load_data("cenas.json")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["Proteina"] == "Huevo"


def test_load_desayunos_data_with_nested_structure(tmp_path, monkeypatch):
    """Prueba cargar datos de desayunos.json que tienen estructura anidada"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)

    file_path = data_dir / "desayunos.json"

    desayunos_data = [
        {
            "data": [
                {
                    "id": 1,
                    "Proteina": "Bistec",
                    "Complemento": "con Hojaldre",
                    "Descripcion": "Bistec Guisado con Hojaldre",
                    "TipoCocionProteina": "Guisado"
                }
            ]
        }
    ]

    file_path.write_text(json.dumps(desayunos_data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = load_data("desayunos.json")

    assert isinstance(result, list)
    assert result[0]["Proteina"] == "Bistec"


def test_load_data_with_plain_list_structure(tmp_path, monkeypatch):
    """Prueba cargar datos con estructura de lista simple"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)

    file_path = data_dir / "simple.json"

    simple_data = [
        {
            "id": 100,
            "Proteina": "Pollo",
            "Complemento": "Arroz",
            "Descripcion": "Pollo asado con arroz",
            "TipoCocionProteina": "Asado"
        }
    ]

    file_path.write_text(json.dumps(simple_data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = load_data("simple.json")

    assert isinstance(result, list)
    assert result[0]["Proteina"] == "Pollo"


def test_load_data_empty_list(tmp_path, monkeypatch):
    """Prueba cargar un archivo con lista vacía"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)

    file_path = data_dir / "empty.json"
    file_path.write_text("[]", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = load_data("empty.json")

    assert isinstance(result, list)
    assert len(result) == 0


def test_load_data_empty_nested_structure(tmp_path, monkeypatch):
    """Prueba cargar estructura anidada vacía"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)

    file_path = data_dir / "empty_nested.json"

    empty_nested_data = [{"data": []}]
    file_path.write_text(json.dumps(empty_nested_data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = load_data("empty_nested.json")

    assert isinstance(result, list)
    assert len(result) == 0


def test_load_data_file_not_found(tmp_path, monkeypatch):
    """Prueba el comportamiento cuando el archivo no existe"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)
    monkeypatch.chdir(tmp_path)

    with pytest.raises(FileNotFoundError):
        load_data("archivo_inexistente.json")


def test_load_data_with_malformed_json(tmp_path, monkeypatch):
    """Prueba el comportamiento con JSON malformado"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)

    file_path = data_dir / "malformed.json"
    file_path.write_text("{malformed json}", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    with pytest.raises(json.JSONDecodeError):
        load_data("malformed.json")


def test_load_data_with_different_structures(tmp_path, monkeypatch):
    """Prueba varios tipos de estructuras de datos"""
    data_dir = tmp_path / "data" / "json"
    data_dir.mkdir(parents=True)
    monkeypatch.chdir(tmp_path)

    # Test 1: Objeto simple (no lista)
    simple_obj = {"id": 1, "name": "test"}
    file_path = data_dir / "object.json"
    file_path.write_text(json.dumps(simple_obj), encoding="utf-8")

    result = load_data("object.json")
    assert isinstance(result, dict)
    assert result["name"] == "test"

    # Test 2: Lista con múltiples elementos anidados
    multi_data = [{"data": [{"id": 1}, {"id": 2}]}]
    file_path = data_dir / "multi.json"
    file_path.write_text(json.dumps(multi_data), encoding="utf-8")

    result = load_data("multi.json")
    assert len(result) == 2
    assert result[0]["id"] == 1
