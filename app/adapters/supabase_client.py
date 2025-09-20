from supabase import create_client, Client
import os

OPERATORS_MAP = {
    "=": "eq",
    "!=": "neq",
    ">": "gt",
    ">=": "gte",
    "<": "lt",
    "<=": "lte",
    "like": "like",
    "in": "in",
}


class SupabaseClient:

    def __init__(self, url: str = None, key: str = None):
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar configurados")
        print(f"URL = {self.url}")
        self.client: Client = create_client(self.url, self.key)

    def fetch_table(self, table: str, limit: int = 100):
        """Consulta registros de una tabla de Supabase"""
        response = self.client.table(table).select("*").limit(limit).execute()
        return response.data

    def parse_where(self, query: str) -> str:
        """
        Convierte un texto de condiciones tipo SQL a formato Supabase.
        Ejemplo: "edad >= 18 AND activo = true OR ciudad = 'Panamá'"
        Salida:  "edad.gte.18,activo.eq.true,ciudad.eq.Panamá"
        """
        # Normalizar texto
        text = query.strip()

        # Reemplazar operadores por formato supabase
        for op, supa_op in OPERATORS_MAP.items():
            text = text.replace(f" {op} ", f".{supa_op}.")

        # Reemplazar AND → nada (porque se pueden encadenar)
        text = text.replace("AND", ",")

        # Reemplazar OR → coma
        text = text.replace("OR", ",")

        # Quitar comillas simples/dobles
        text = text.replace("'", "").replace('"', "")

        return text

    def select_table(self, table: str, where: str, columns: str = "*"):
        """
        Ejecuta un SELECT con condiciones pasadas como texto.
        """
        condition = self.parse_where(where)
        query = self.client.table(table).select(columns)

        if "," in condition:  # varias condiciones -> OR
            response = query.or_(condition).execute()
        else:  # condición única -> filter(col, op, val)
            parts = condition.split(".")
            if len(parts) == 3:
                col, op, val = parts
                response = query.filter(col, op, val).execute()
            else:
                raise ValueError(f"Formato de condición no válido: {condition}")

        return response.data
