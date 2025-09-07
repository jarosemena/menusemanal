from app.use_cases.process_data import generate_weekly_menu

if __name__ == "__main__":
    menu_semanal = generate_weekly_menu()

    for dia in menu_semanal:
        print(f"{dia['DiaSemana']}:")
        print(f"  Desayuno: {dia['DescDesayuno']}")
        print(f"  Almuerzo: {dia['DescAlmuerzo']}")
        print(f"  Cena: {dia['DescCena']}")
        print()
