app/adapters/ → aquí van las integraciones externas (Supabase en tu caso).

app/domain/ → reglas de negocio (no necesita conexión directa a Supabase).

app/use_cases/ → orquestadores, llaman a los adapters y aplican la lógica de negocio.

app/tests/ → tus pruebas unitarias/integración.