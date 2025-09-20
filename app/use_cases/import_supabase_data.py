import json
import os
from app.adapters.supabase_client import SupabaseClient


class SupabaseImporter:

    def __init__(self, output_dir: str = "data/json"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.client = SupabaseClient()
        

    def import_table(self, table: str, limit: int = 100):
        """Exporta datos de Supabase a un archivo JSON"""
        data = self.client.fetch_table(table, limit=limit)

        output_path = os.path.join(self.output_dir, f"{table.lower()}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return output_path

    def import_Select_table(self, table: str, where: str, limit: int = 100):
        """Exporta datos de Supabase a un archivo JSON"""
        data = self.client.select_table(table, where)

        output_path = os.path.join(self.output_dir, f"{table.lower()}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return output_path
