import random
from typing import List, Dict
from datetime import date, timedelta


class MenuGenerator:
    def __init__(self, desayunos: List[Dict], almuerzos: List[Dict],
                 cenas: List[Dict], menu_anterior: List[Dict] = None,
                 idsemana: str = None, fecha_lunes: date = date.today()):
        self.desayunos = desayunos
        self.almuerzos = almuerzos
        self.cenas = cenas
        self.menu_anterior = menu_anterior or []
        self.idsemana = idsemana
        self.fecha_lunes = fecha_lunes
        self.proteinas_recientes = []
        self.complementos_almuerzos = set()
        self.complementos_cenas = set()
        self.complementos_desayunos = set()

    def _filtrar_por_repeticion(self, opciones: List[Dict], tipo_comida: str,
                                dia: int) -> List[Dict]:
        if not self.menu_anterior or dia >= len(self.menu_anterior):
            return opciones

        codigo_anterior = None
        dia_anterior = self.menu_anterior[dia]  # Ahora seguro que existe

        if tipo_comida == 'desayuno':
            codigo_anterior = dia_anterior.get('CodigoDesayuno')
        elif tipo_comida == 'almuerzo':
            codigo_anterior = dia_anterior.get('CodigoAlmuerzo')
        elif tipo_comida == 'cena':
            codigo_anterior = dia_anterior.get('CodigoCena')

        if codigo_anterior is None:
            return opciones

        return [op for op in opciones if op['id'] != codigo_anterior]

    def _filtrar_proteina_reciente(self, opciones: List[Dict]) -> List[Dict]:
        if len(self.proteinas_recientes) < 2:
            return opciones

        ultimas_proteinas = set(self.proteinas_recientes[-2:])
        if len(ultimas_proteinas) == 1:
            return [op for op in opciones if op['Proteina'] not in ultimas_proteinas]
        return opciones

    def _seleccionar_opcion(self, opciones: List[Dict], tipo_comida: str, dia: int) -> Dict:
        opciones_filtradas = self._filtrar_por_repeticion(opciones, tipo_comida, dia)
        opciones_filtradas = self._filtrar_proteina_reciente(opciones_filtradas)

        if tipo_comida == 'almuerzo':
            opciones_filtradas = [op for op in opciones_filtradas
                                  if op['Complemento'] not in self.complementos_almuerzos]
        elif tipo_comida == 'cena':
            opciones_filtradas = [op for op in opciones_filtradas
                                  if op['Complemento'] not in self.complementos_cenas]
        elif tipo_comida == 'desayuno':
            opciones_filtradas = [op for op in opciones_filtradas
                                  if op['Complemento'] not in self.complementos_desayunos]

        if not opciones_filtradas:
            return random.choice(opciones)

        return random.choice(opciones_filtradas)

    def dia_a_indice_simple(self, dia_texto: str, dias_semana: list[str]) -> int:
        for i, dia in enumerate(dias_semana):
            if dia.lower() == dia_texto.lower():
                return i
        return 0

    def generar_menu_semanal(self) -> List[Dict]:
        menu = []
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

        # Preparar almuerzos base para los pares de días
        if len(self.almuerzos) >= 3:
            almuerzos_base = random.sample(self.almuerzos, 3)
        else:
            almuerzos_base = self.almuerzos * 3
            almuerzos_base = almuerzos_base[:3]

        # Diccionario para mapear qué almuerzo base usar para cada día
        almuerzo_por_dia = {
            'Lunes': almuerzos_base[0],
            'Martes': almuerzos_base[1],
            'Miércoles': almuerzos_base[0],  # Mismo que Lunes
            'Jueves': almuerzos_base[1],     # Mismo que Martes
            'Viernes': almuerzos_base[2],
            'Sábado': almuerzos_base[2],     # Mismo que Viernes
            'Domingo': None  # Se seleccionará individualmente
        }

        for i, dia in enumerate(dias_semana):
            # Seleccionar desayuno y cena únicos para cada día
            desayuno = self._seleccionar_opcion(self.desayunos, 'desayuno', i)

            if dia == 'Domingo':
                almuerzo = self._seleccionar_opcion(self.almuerzos, 'almuerzo', i)
            else:
                almuerzo = almuerzo_por_dia[dia]

            cena = self._seleccionar_opcion(self.cenas, 'cena', i)

            # Actualizar registros de proteínas y complementos
            self.proteinas_recientes.extend([desayuno['Proteina'],
                                            almuerzo['Proteina'], cena['Proteina']])
            self.complementos_almuerzos.add(almuerzo['Complemento'])
            self.complementos_cenas.add(cena['Complemento'])
            self.complementos_desayunos.add(desayuno['Complemento'])

            if len(self.proteinas_recientes) > 6:
                self.proteinas_recientes = self.proteinas_recientes[-6:]
            
            daystosum = self.dia_a_indice_simple(dia, dias_semana)
            print(f" daystosum = {daystosum}")
            if (daystosum > 0):
                fecha: date = self.fecha_lunes + timedelta(days=daystosum)
            else:
                fecha: date = self.fecha_lunes
            if (dia == "Domingo"):
                menu.append({
                    'IDSemana': self.idsemana,
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
                    'IDSemana': self.idsemana,
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
