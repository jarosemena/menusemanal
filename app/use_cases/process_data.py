from app.adapters.storage import load_data
from app.domain.services import MenuGenerator


def generate_weekly_menu(menu_anterior=None):
    desayunos = load_data("desayunos.json")
    almuerzos = load_data("almuerzos.json")
    cenas = load_data("cenas.json")

    generador = MenuGenerator(desayunos, almuerzos, cenas, menu_anterior or [])
    return generador.generar_menu_semanal()
