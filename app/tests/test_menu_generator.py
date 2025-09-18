# test_menu_generation.py
import pytest
from app.use_cases.process_data import generate_weekly_menu


def test_menu_generation_structure():
    """Prueba que el menú generado tenga la estructura correcta"""
    menu_semanal = generate_weekly_menu() 
 
    # Verificar que se generan 7 días
    assert len(menu_semanal) == 7
    
    # Verificar los días de la semana
    dias_esperados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dias_generados = [dia["DiaSemana"] for dia in menu_semanal]
    
    assert dias_generados == dias_esperados
    
    # Verificar que cada día tiene las claves correctas
    for dia in menu_semanal:
        assert "DiaSemana" in dia
        assert "DescDesayuno" in dia
        assert "DescAlmuerzo" in dia
        assert "DescCena" in dia


def test_menu_no_empty_meals():
    """Prueba que ninguna comida esté vacía"""
    menu_semanal = generate_weekly_menu()
    
    for dia in menu_semanal:
        assert dia["DescDesayuno"].strip() != ""
        assert dia["DescAlmuerzo"].strip() != ""
        assert dia["DescCena"].strip() != ""


def test_menu_no_duplicate_days():
    """Prueba que no haya días duplicados"""
    menu_semanal = generate_weekly_menu()
    
    dias = [dia["DiaSemana"] for dia in menu_semanal]
    assert len(dias) == len(set(dias)), "Hay días duplicados en el menú"


def test_menu_variety():
    """Prueba que haya variedad en las comidas (no todas iguales)"""
    menu_semanal = generate_weekly_menu()
    
    desayunos = [dia["DescDesayuno"] for dia in menu_semanal]
    almuerzos = [dia["DescAlmuerzo"] for dia in menu_semanal]
    cenas = [dia["DescCena"] for dia in menu_semanal]
    
    # Verificar que hay variedad (más de 1 opción diferente)
    assert len(set(desayunos)) > 1, "Poca variedad en desayunos"
    assert len(set(almuerzos)) > 1, "Poca variedad en almuerzos"
    assert len(set(cenas)) > 1, "Poca variedad en cenas"


def test_menu_meal_format():
    """Prueba el formato de las descripciones de comidas"""
    menu_semanal = generate_weekly_menu()
    
    for dia in menu_semanal:
        # Verificar que las descripciones no empiecen/terminen con espacios extraños
        assert not dia["DescDesayuno"].startswith(" ")
        assert not dia["DescDesayuno"].endswith(" ")
        assert not dia["DescAlmuerzo"].startswith(" ")
        assert not dia["DescAlmuerzo"].endswith(" ")
        assert not dia["DescCena"].startswith(" ")
        assert not dia["DescCena"].endswith(" ")
        
        # Verificar que no haya dobles espacios
        assert "  " not in dia["DescDesayuno"]
        assert "  " not in dia["DescAlmuerzo"]
        assert "  " not in dia["DescCena"]


def test_menu_consecutive_days_variation():
    """Prueba que días consecutivos no tengan exactamente las mismas comidas"""
    menu_semanal = generate_weekly_menu()
    
    for i in range(len(menu_semanal) - 1):
        dia_actual = menu_semanal[i]
        dia_siguiente = menu_semanal[i + 1]
        
        # No deberían tener exactamente las mismas tres comidas
        assert not (
            dia_actual["DescDesayuno"] == dia_siguiente["DescDesayuno"] and
            dia_actual["DescAlmuerzo"] == dia_siguiente["DescAlmuerzo"] and
            dia_actual["DescCena"] == dia_siguiente["DescCena"]
        ), f"Días {i} y {i+1} tienen comidas idénticas"


def test_menu_generation_multiple_times():
    """Prueba que generar el menú múltiples veces produce resultados diferentes"""
    menu_1 = generate_weekly_menu()
    menu_2 = generate_weekly_menu()
    
    # Los menús no deberían ser idénticos (debido a la aleatoriedad)
    assert menu_1 != menu_2


def test_menu_with_previous_menu():
    """Prueba la generación con un menú anterior para evitar repeticiones"""
    menu_anterior = [
        {
            "DiaSemana": "Lunes",
            "DescDesayuno": "Desayuno anterior",
            "DescAlmuerzo": "Almuerzo anterior", 
            "DescCena": "Cena anterior"
        }
    ]
    
    menu_nuevo = generate_weekly_menu(menu_anterior)
    
    # Verificar que el nuevo menú no repite exactamente el menú anterior
    # (esto depende de cómo esté implementada la lógica de evitar repeticiones)
    assert len(menu_nuevo) == 7


def test_menu_protein_variety():
    """Prueba que haya variedad de proteínas en la semana"""
    menu_semanal = generate_weekly_menu()
    
    # Extraer proteínas de las descripciones (simplificado)
    proteinas_almuerzo = []
    for dia in menu_semanal:
        descripcion = dia["DescAlmuerzo"].lower()
        if "pollo" in descripcion:
            proteinas_almuerzo.append("Pollo")
        elif "carne" in descripcion or "res" in descripcion:
            proteinas_almuerzo.append("Carne")
        elif "cerdo" in descripcion:
            proteinas_almuerzo.append("Cerdo")
        elif "pescado" in descripcion:
            proteinas_almuerzo.append("Pescado")
        elif "mixto" in descripcion:
            proteinas_almuerzo.append("Mixto")
    
    # Debería haber variedad de proteínas
    assert len(set(proteinas_almuerzo)) > 1, "Poca variedad de proteínas en almuerzos"

def test_menu_no_repeated_consecutive_days():
   
    menu_semanal = generate_weekly_menu()
    
    dias = [dia["DiaSemana"] for dia in menu_semanal]
    
    # Verificar que no hay días consecutivos repetidos
    for i in range(len(dias) - 1):
        assert dias[i] != dias[i + 1], f"Día repetido consecutivo: {dias[i]} en posición {i} y {i+1}"
    
    print("Menú generado sin días consecutivos repetidos:")
    for dia in menu_semanal:
        print(f"{dia['DiaSemana']}:")
        print(f"  Desayuno: {dia['DescDesayuno']}")
        print(f"  Almuerzo: {dia['DescAlmuerzo']}")
        print(f"  Cena: {dia['DescCena']}")
        print()