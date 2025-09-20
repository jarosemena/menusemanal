import json
import functions_framework
from app.use_cases.process_data import generate_weekly_menu
from dotenv import load_dotenv
load_dotenv()

@functions_framework.http
def get_menu(request):
    """HTTP Cloud Function con Flask-like request handling"""
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return ('', 204, headers)

    try:
        # Parse query parameters or JSON body
        if request.method == 'GET':
            menu_semanal = generate_weekly_menu()

            response_data = {
                "status": "success",
                "data": menu_semanal,
                "count": len(menu_semanal)
            }

            headers['Content-Type'] = 'application/json'
            json_data = json.dumps(response_data)

            return json_data, 200, {'Content-Type': 'application/json'}
        else:
            return (json.dumps("Only be Able the Get Metod"), 400, headers)

    except Exception as e:
        error_response = {
            "status": "error",
            "message": str(e)
        }
        return (json.dumps(error_response), 500, headers)


def get_menu_local():
    menu_semanal = generate_weekly_menu()

    for dia in menu_semanal:
        print(f"idsemana: {dia['IDSemana']}")
        print(f"fecha: {dia['Fecha']}")
        print(f"{dia['DiaSemana']}:")
        print(f"  Desayuno: {dia['DescDesayuno']}")
        print(f"  Almuerzo: {dia['DescAlmuerzo']}")
        print(f"  Cena: {dia['DescCena']}")
        print()


if __name__ == "__main__":
    get_menu_local()
