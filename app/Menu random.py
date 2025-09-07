import random
from typing import List, Dict, Tuple
import json

class MenuGenerator:
    def __init__(self, desayunos: List[Dict], almuerzos: List[Dict], cenas: List[Dict], menu_anterior: List[Dict] = None):
        self.desayunos = desayunos
        self.almuerzos = almuerzos
        self.cenas = cenas
        self.menu_anterior = menu_anterior or []
        
        # Estructura para tracking de restricciones
        self.proteinas_recientes = []
        self.complementos_almuerzos = set()
        self.complementos_cenas = set()
        self.complementos_desayunos = set()

    def _filtrar_por_repeticion(self, opciones: List[Dict], tipo_comida: str, dia: int) -> List[Dict]:
        """Filtra opciones que no estén en el menú anterior mismo día"""
        if not self.menu_anterior:
            return opciones
            
        # Obtener código del mismo día semana anterior
        codigo_anterior = None
        if tipo_comida == 'desayuno':
            codigo_anterior = self.menu_anterior[dia].get('CodigoDesayuno')
        elif tipo_comida == 'almuerzo':
            codigo_anterior = self.menu_anterior[dia].get('CodigoAlmuerzo')
        elif tipo_comida == 'cena':
            codigo_anterior = self.menu_anterior[dia].get('CodigoCena')
            
        return [op for op in opciones if op['id'] != codigo_anterior]

    def _filtrar_proteina_reciente(self, opciones: List[Dict]) -> List[Dict]:
        """Filtra opciones que rompan la regla de 3 días consecutivos misma proteína"""
        if len(self.proteinas_recientes) < 2:
            return opciones
            
        # Obtener últimas 2 proteínas
        ultimas_proteinas = set(self.proteinas_recientes[-2:])
        if len(ultimas_proteinas) == 1:
            return [op for op in opciones if op['Proteina'] not in ultimas_proteinas]
        return opciones

    def _seleccionar_opcion(self, opciones: List[Dict], tipo_comida: str, dia: int) -> Dict:
        """Selecciona una opción validando todas las restricciones"""
        # Filtrar por repetición semana anterior
        opciones_filtradas = self._filtrar_por_repeticion(opciones, tipo_comida, dia)
        
        # Filtrar por proteínas recientes
        opciones_filtradas = self._filtrar_proteina_reciente(opciones_filtradas)
        
        # Filtrar por complementos únicos esta semana
        if tipo_comida == 'almuerzo':
            opciones_filtradas = [op for op in opciones_filtradas if op['Complemento'] not in self.complementos_almuerzos]
        elif tipo_comida == 'cena':
            opciones_filtradas = [op for op in opciones_filtradas if op['Complemento'] not in self.complementos_cenas]
        elif tipo_comida == 'desayuno':
            opciones_filtradas = [op for op in opciones_filtradas if op['Complemento'] not in self.complementos_desayunos]
        
        if not opciones_filtradas:
            # Relajar restricciones de complementos si no hay opciones
            return random.choice(opciones)
            
        return random.choice(opciones_filtradas)

    def generar_menu_semanal(self) -> List[Dict]:
        menu = []
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        # Almuerzos especiales (solo 3 únicos)
        almuerzos_base = random.sample(self.almuerzos, 3)
        
        for i, dia in enumerate(dias_semana):
            # Determinar patrones de repetición
            if dia in ['Martes', 'Jueves']:
                # Usar mismo menú que el día correspondiente
                menu_duplicado = menu[i-2] if i >= 2 else None
                if menu_duplicado:
                    menu.append(menu_duplicado)
                    continue

            # Seleccionar desayuno
            desayuno = self._seleccionar_opcion(self.desayunos, 'desayuno', i)
            
            # Seleccionar almuerzo según día
            if dia in ['Lunes', 'Miércoles']:
                almuerzo = almuerzos_base[0]
            elif dia in ['Martes', 'Jueves']:
                almuerzo = almuerzos_base[1]
            elif dia in ['Viernes', 'Sábado']:
                almuerzo = almuerzos_base[2]
            else:  # Domingo
                almuerzo = self._seleccionar_opcion(self.almuerzos, 'almuerzo', i)
            
            # Seleccionar cena
            cena = self._seleccionar_opcion(self.cenas, 'cena', i)
            
            # Actualizar trackers
            self.proteinas_recientes.append(desayuno['Proteina'])
            self.proteinas_recientes.append(almuerzo['Proteina'])
            self.proteinas_recientes.append(cena['Proteina'])
            
            self.complementos_almuerzos.add(almuerzo['Complemento'])
            self.complementos_cenas.add(cena['Complemento'])
            self.complementos_desayunos.add(desayuno['Complemento'])
            
            # Mantener solo últimos 6 días de proteínas (2 días completos)
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

# Ejemplo de uso:
if __name__ == "__main__":
    # Datos de ejemplo (deben ser reemplazados con datos reales)
    with open("desayunos.json", "r", encoding="utf-8") as f:
        desayunos = json.load(f)
        # Extraer la lista dentro de "data"
        if isinstance(desayunos, list) and "data" in desayunos[0]:
            desayunos = desayunos[0]["data"]

    with open("almuerzos.json", "r", encoding="utf-8") as f:
        almuerzos = json.load(f)
        # Extraer la lista dentro de "data"
        if isinstance(almuerzos, list) and "data" in almuerzos[0]:
            almuerzos = almuerzos[0]["data"]

    with open("cenas.json", "r", encoding="utf-8") as f:
        cenas = json.load(f)   
        # Extraer la lista dentro de "data"
        if isinstance(cenas, list) and "data" in cenas[0]:
            cenas = cenas[0]["data"] 
   
    
    # Menu anterior (semana pasada)
    menu_anterior = [
        # ... datos del menú anterior
    ]
    
    generador = MenuGenerator(desayunos, almuerzos, cenas, menu_anterior)
    menu_semanal = generador.generar_menu_semanal()
    
    # Imprimir resultado
    for dia in menu_semanal:
        print(f"{dia['DiaSemana']}:")
        print(f"  Desayuno: {dia['DescDesayuno']}")
        print(f"  Almuerzo: {dia['DescAlmuerzo']}")
        print(f"  Cena: {dia['DescCena']}")
        print()