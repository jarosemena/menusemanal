from app.adapters.storage import load_data
from app.domain.services import MenuGenerator
from app.domain.get_informacion_fecha import InformacionFecha


def generate_weekly_menu(menu_anterior=None):
    desayunos = load_data("desayunos.json")
    almuerzos = load_data("almuerzos.json")
    cenas = load_data("cenas.json")
    menu_anterior = []

    fechas = InformacionFecha()

    generador = MenuGenerator(desayunos, almuerzos, cenas,
     menu_anterior, fechas.codigo_de_semana, fechas.fecha_del_siguiente_lunes)

    return generador.generar_menu_semanal()
