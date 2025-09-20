import os
import json
import pytest
from app.use_cases.import_supabase_data import SupabaseImporter
from dotenv import load_dotenv
load_dotenv()


@pytest.fixture
def importer(tmp_path):
    return SupabaseImporter(output_dir=tmp_path)


def test_import_table_Almuerzo_file(importer):
    path = importer.import_table("Almuerzos", limit=10000)
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)


def test_import_table_Cena_json(importer):
    path = importer.import_table("Cenas", limit=10000)
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)


def test_import_table_Desayuno_json(importer):
    path = importer.import_table("Desayunos", limit=10000)
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)


def test_import_table_menuanterior_json(importer):
    path = importer.import_Select_table("MenuSemanal", "IDSemana = '2025-13'", limit=10000)
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
