import random
from typing import List, Dict


class MenuGenerator:
    def __init__(self, desayunos: List[Dict], almuerzos: List[Dict], cenas: List[Dict], menu_anterior: List[Dict] = None):
        self.desayunos = desayunos
        self.almuerzos = almuerzos
        self.cenas = cenas
        self.menu_anterior = menu_anterior or []

        self.proteinas_recientes = []
        self.complementos_almuerzos = set()
        self.complementos_cenas = set()
        self.complementos_desayunos = set()

    def _filtrar_por_repeticion(self, opciones: List[Dict], tipo_comida: str, dia: int) -> List[Dict]:
        if not self.menu_anterior:
            return opciones

        codigo_anterior = None
        if tipo_comida == 'desayuno':
            codigo_anterior = self.menu_anterior[dia].get('CodigoDesayuno')
        elif tipo_comida == 'almuerzo':
            codigo_anterior = self.menu_anterior[dia].get('CodigoAlmuerzo')
        elif tipo_comida == 'cena':
            codigo_anterior = self.menu_anterior[dia].get('CodigoCena')

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
            opciones_filtradas = [op for op in opciones_filtradas if op['Complemento'] not in self.complementos_almuerzos]
        elif tipo_comida == 'cena':
            opciones_filtradas = [op for op in opciones_filtradas if op['Complemento'] not in self.complementos_cenas]
        elif tipo_comida == 'desayuno':
            opciones_filtradas = [op for op in opciones_filtradas if op['Complemento'] not in self.complementos_desayunos]

        if not opciones_filtradas:
            return random.choice(opciones)

        return random.choice(opciones_filtradas)

    def generar_menu_semanal(self) -> List[Dict]:
        menu = []
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        almuerzos_base = random.sample(self.almuerzos, 3)

        for i, dia in enumerate(dias_semana):
            if dia in ['Martes', 'Jueves'] and i >= 2:
                menu.append(menu[i-2])
                continue

            desayuno = self._seleccionar_opcion(self.desayunos, 'desayuno', i)

            if dia in ['Lunes', 'Miércoles']:
                almuerzo = almuerzos_base[0]
            elif dia in ['Martes', 'Jueves']:
                almuerzo = almuerzos_base[1]
            elif dia in ['Viernes', 'Sábado']:
                almuerzo = almuerzos_base[2]
            else:
                almuerzo = self._seleccionar_opcion(self.almuerzos, 'almuerzo', i)

            cena = self._seleccionar_opcion(self.cenas, 'cena', i)

            self.proteinas_recientes.extend([desayuno['Proteina'], almuerzo['Proteina'], cena['Proteina']])
            self.complementos_almuerzos.add(almuerzo['Complemento'])
            self.complementos_cenas.add(cena['Complemento'])
            self.complementos_desayunos.add(desayuno['Complemento'])

            if len(self.proteinas_recientes) > 6:
                self.proteinas_recientes = self.proteinas_recientes[-6:]

            menu.append({
                'DiaSemana': dia,
                'CodigoDesayuno': desayuno['id'],
                'DescDesayuno': desayuno['Descripcion'],
                'CodigoAlmuerzo': almuerzo['id'],
                'DescAlmuerzo': almuerzo['Descripcion'],
                'CodigoCena': cena['id'],
                'DescCena': cena['Descripcion']
            })

        return menu
