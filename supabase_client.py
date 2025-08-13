from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Defina SUPABASE_URL e SUPABASE_KEY no .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_contacts(limit=3):
    resp = supabase.table("contatos").select("*").limit(3).execute()
    print(resp.data)
    if hasattr(resp, 'error') and resp.error:
        raise RuntimeError(f"Erro ao buscar contatos: {resp.error}")
    return resp.data
