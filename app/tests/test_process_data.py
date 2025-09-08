import pytest
from app.use_cases.process_data import generate_weekly_menu


@pytest.fixture
def mock_storage(monkeypatch):
    def fake_load_data(file_name):
        if "desayunos" in file_name:
            return [{"id": 1, "Proteina": "Huevo", "Complemento": "Pan", "Descripcion": "Huevos"}]
        if "almuerzos" in file_name:
            return [{"id": 10, "Proteina": "Pollo", "Complemento": "Arroz", "Descripcion": "Pollo"}]
        if "cenas" in file_name:
            return [{"id": 20, "Proteina": "Carne", "Complemento": "Pasta", "Descripcion": "Carne con pasta"}]
    monkeypatch.setattr("app.use_cases.process_data.load_data", fake_load_data)


def test_generate_weekly_menu(mock_storage):
    menu = generate_weekly_menu()
    assert len(menu) == 7
    assert all("DiaSemana" in dia for dia in menu)
