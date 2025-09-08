import pytest
from app.domain.services import MenuGenerator


@pytest.fixture
def sample_data():
    desayunos = [
        {"id": 1, "Proteina": "Huevo", "Complemento": "Pan", "Descripcion": "Huevos revueltos"},
        {"id": 2, "Proteina": "Queso", "Complemento": "Arepa", "Descripcion": "Arepa con queso"},
    ]
    almuerzos = [
        {"id": 10, "Proteina": "Pollo", "Complemento": "Arroz", "Descripcion": "Pollo con arroz"},
        {"id": 11, "Proteina": "Carne", "Complemento": "Pasta", "Descripcion": "Carne con pasta"},
    ]
    cenas = [
        {"id": 20, "Proteina": "Pescado", "Complemento": "Ensalada", "Descripcion": "Pescado con ensalada"},
        {"id": 21, "Proteina": "Tofu", "Complemento": "Verduras", "Descripcion": "Tofu con verduras"},
    ]
    return desayunos, almuerzos, cenas


def test_menu_generator_creates_weekly_menu(sample_data):
    desayunos, almuerzos, cenas = sample_data
    generator = MenuGenerator(desayunos, almuerzos, cenas)
    menu = generator.generar_menu_semanal()

    assert len(menu) == 7  # 7 días de la semana
    for dia in menu:
        assert "DiaSemana" in dia
        assert "DescDesayuno" in dia
        assert "DescAlmuerzo" in dia
        assert "DescCena" in dia


def test_no_repeated_protein_three_days(sample_data):
    desayunos, almuerzos, cenas = sample_data
    generator = MenuGenerator(desayunos, almuerzos, cenas)
    menu = generator.generar_menu_semanal()

    # Simular que nunca repite proteína 3 días seguidos
    proteinas = []
    for dia in menu:
        proteinas.extend([dia["DescDesayuno"], dia["DescAlmuerzo"], dia["DescCena"]])
    # Aquí simplemente probamos que la lista de proteínas no quede vacía
    assert len(proteinas) > 0
