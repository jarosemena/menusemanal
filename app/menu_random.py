import random
from typing import List, Dict, Tuple
import json
from datetime import date ,timedelta


selfdesayunos = None
selfalmuerzos = None
selfcenas = None
selfmenu_anterior = []
selfidsemana: str = ""
selffecha_lunes: date = date.today()
# Estructura para tracking de restricciones
selfproteinas_recientes = []
selfcomplementos_almuerzos = set()
selfcomplementos_cenas = set()
selfcomplementos_desayunos = set()

def define_variabels(desayunos,almuerzos,cenas,menu_anterior,idsemana,fecha_lunes):
    global selfdesayunos, selfalmuerzos, selfcenas, selfmenu_anterior, selfidsemana, selffecha_lunes
    selfdesayunos = desayunos
    selfalmuerzos = almuerzos
    selfcenas = cenas
    selfmenu_anterior = menu_anterior or []
    selfidsemana = idsemana
    selffecha_lunes = fecha_lunes     


def _filtrar_por_repeticion( opciones: List[Dict], tipo_comida: str, dia: int) -> List[Dict]:
    """Filtra opciones que no estén en el menú anterior mismo día"""
    if not selfmenu_anterior:
        return opciones
        
    # Obtener código del mismo día semana anterior
    codigo_anterior = None
    if tipo_comida == 'desayuno':
        codigo_anterior = selfmenu_anterior[dia].get('CodigoDesayuno')
    elif tipo_comida == 'almuerzo':
        codigo_anterior = selfmenu_anterior[dia].get('CodigoAlmuerzo')
    elif tipo_comida == 'cena':
        codigo_anterior = selfmenu_anterior[dia].get('CodigoCena')
        
    return [op for op in opciones if op['id'] != codigo_anterior]

def _filtrar_proteina_reciente(opciones: List[Dict]) -> List[Dict]:
    """Filtra opciones que rompan la regla de 3 días consecutivos misma proteína"""
    if len(selfproteinas_recientes) < 2:
        return opciones
        
    # Obtener últimas 2 proteínas
    ultimas_proteinas = set(selfproteinas_recientes[-2:])
    if len(ultimas_proteinas) == 1:
        return [op for op in opciones if op['Proteina'] not in ultimas_proteinas]
    return opciones

def _seleccionar_opcion(opciones: List[Dict], tipo_comida: str, dia: int) -> Dict:
    """Selecciona una opción validando todas las restricciones"""
    # Filtrar por repetición semana anterior
    opciones_filtradas = _filtrar_por_repeticion(opciones, tipo_comida, dia)   
    # Filtrar por proteínas recientes
    opciones_filtradas = _filtrar_proteina_reciente(opciones_filtradas)
   
    # Filtrar por complementos únicos esta semana
    if tipo_comida == 'almuerzo':
        opciones_filtradas = [op for op in opciones_filtradas if op['Complemento'] not in selfcomplementos_almuerzos]
    elif tipo_comida == 'cena':
        opciones_filtradas = [op for op in opciones_filtradas if op['Complemento'] not in selfcomplementos_cenas]
    elif tipo_comida == 'desayuno':
        opciones_filtradas = [op for op in opciones_filtradas if op['Complemento'] not in selfcomplementos_desayunos]
    
    if not opciones_filtradas:
        # Relajar restricciones de complementos si no hay opciones
        return random.choice(opciones)
        
    return random.choice(opciones_filtradas)

def dia_a_indice_simple(dia_texto: str, dias_semana: list[str]) -> int:
    for i, dia in enumerate(dias_semana):
        if dia.lower() == dia_texto.lower():
            return i
    return 0

def generar_menu_semanal() -> List[Dict]:    
    global selfproteinas_recientes, selfcomplementos_almuerzos, selfcomplementos_cenas, selfcomplementos_desayunos
    # Reset trackers
    selfproteinas_recientes = []
    selfcomplementos_almuerzos = set()
    selfcomplementos_cenas = set()
    selfcomplementos_desayunos = set()

    menu = []
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    # Almuerzos especiales (solo 3 únicos)
    almuerzos_base = random.sample(selfalmuerzos, 3)
    
    for i, dia in enumerate(dias_semana):
        # Determinar patrones de repetición
        if dia in ['Miércoles', 'Jueves', 'Sabado']:
            # Usar mismo menú que el día correspondiente
            menu_duplicado = menu[i-2] if i >= 2 else None
            if menu_duplicado:
                menu_duplicado['DiaSemana'] = dia
                menu.append(menu_duplicado)
                continue

        # Seleccionar desayuno
        desayuno = _seleccionar_opcion(selfdesayunos, 'desayuno', i)
        
        # Seleccionar almuerzo según día
        if dia in ['Lunes', 'Miércoles']:
            almuerzo = almuerzos_base[0]
        elif dia in ['Martes', 'Jueves']:
            almuerzo = almuerzos_base[1]
        elif dia in ['Viernes', 'Sábado']:
            almuerzo = almuerzos_base[2]
        else:  # Domingo
            almuerzo = _seleccionar_opcion(selfalmuerzos, 'almuerzo', i)
        
        # Seleccionar cena
        cena = _seleccionar_opcion(selfcenas, 'cena', i)
        
        # Actualizar trackers
        selfproteinas_recientes.append(desayuno['Proteina'])
        selfproteinas_recientes.append(almuerzo['Proteina'])
        selfproteinas_recientes.append(cena['Proteina'])
        
        selfcomplementos_almuerzos.add(almuerzo['Complemento'])
        selfcomplementos_cenas.add(cena['Complemento'])
        selfcomplementos_desayunos.add(desayuno['Complemento'])
        
        # Mantener solo últimos 6 días de proteínas (2 días completos)
        if len(selfproteinas_recientes) > 6:
            selfproteinas_recientes = selfproteinas_recientes[-6:]
        
        daystosum = dia_a_indice_simple(dia, dias_semana)
        print( f" daystosum = {daystosum}"  )
        if (daystosum > 0):
            fecha: date  = selffecha_lunes + timedelta(days=daystosum )
        else:
            fecha: date  = selffecha_lunes
        if (dia == "Domingo"):
            menu.append({
                'IDSemana': selfidsemana,
                'Fecha': fecha,
                'DiaSemana': dia,
                'CodigoDesayuno': 0,
                'DescDesayuno': "LIBRE",
                'CodigoAlmuerzo': 0,
                'DescAlmuerzo': "LIBRE",
                'CodigoCena': 0,
                'DescCena': "LIBRE"
            })
        else:
            menu.append({
                'IDSemana': selfidsemana,
                'Fecha': fecha,
                'DiaSemana': dia,
                'CodigoDesayuno': desayuno['id'],
                'DescDesayuno': desayuno['Descripcion'],
                'CodigoAlmuerzo': almuerzo['id'],
                'DescAlmuerzo': almuerzo['Descripcion'],
                'CodigoCena': cena['id'],
                'DescCena': cena['Descripcion']
            })
    
    return menu
    

def load_data( path: str):
    with open(path, "r", encoding="utf-8") as f:
        # Caso 1: [{ "data": [...] }]
        data = json.load(f)

        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "data" in data[0]:
            return data[0]["data"]

        # Caso 2: {"data": [...]}
        if isinstance(data, dict) and "data" in data:
            return data["data"]

        # Caso 3: lista directa de objetos
        if isinstance(data, list):
            return data

        raise ValueError(f"Formato inesperado en {path}: {type(data)}")

def get_data( json_string: str):
    data = json.load(json_string)

    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "data" in data[0]:
        return data[0]["data"]

    # Caso 2: {"data": [...]}
    if isinstance(data, dict) and "data" in data:
        return data["data"]

    # Caso 3: lista directa de objetos
    if isinstance(data, list):
        return data

    raise ValueError(f"Formato inesperado en {json_string}: {type(data)}")

# Ejemplo de uso:

def run_python():
    

    desayunos = load_data("desayunos.json")
    almuerzos = load_data("almuerzos.json")
    cenas = load_data("cenas.json") 
    menu_anterior = load_data("menu_anterior.json") 
    fecha_lunes = date.fromisoformat('2025-09-01')
    ##define_variabels('2025-36',fecha_lunes,desayunos, almuerzos, cenas, menu_anterior)
    define_variabels(desayunos, almuerzos, cenas, menu_anterior, '2025-36', fecha_lunes)

    menu_semanal = generar_menu_semanal()
    return menu_semanal 

def run_in_n8n():
    None
   # desayunos = get_data($input.first().json.data)
   # almuerzos = get_data($input.first().json.data)
   # cenas = get_data($input.first().json.data) 
   # menu_anterior = load_data("menu_anterior.json") 
   # fecha_lunes = date.fromisoformat($('Aggregate').first().json.data[3]['Fecha del siguiente lunes'])
   # define_variabels(desayunos, almuerzos, cenas, menu_anterior, $('Aggregate').first().json.data[4]['Código de semana'], fecha_lunes)
   # menu_semanal = generar_menu_semanal()
   # return menu_semanal 


menu_semanal = run_python()
# Imprimir resultado
for dia in menu_semanal:
    print(f"{dia['DiaSemana']}:")
    print(f"  ID_Semana: {dia['IDSemana']}")
    print(f"  Fecha: {dia['Fecha']}")
    print(f"  Desayuno: {dia['DescDesayuno']}")
    print(f"  Almuerzo: {dia['DescAlmuerzo']}")
    print(f"  Cena: {dia['DescCena']}")
    print()

#return run_in_n8n()