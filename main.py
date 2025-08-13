import os
import time
import logging
from dotenv import load_dotenv
import requests

from supabase_client import fetch_contacts
from utils import normalize_phone

# vai carregar as variáveis do arquivo .env
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
ZAPI_INSTANCE = os.environ.get("ZAPI_INSTANCE")
ZAPI_TOKEN = os.environ.get("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.environ.get("ZAPI_CLIENT_TOKEN")
MAX_TO_SEND = int(os.environ.get("MAX_TO_SEND", "3"))

if not (SUPABASE_URL and SUPABASE_KEY):
    raise RuntimeError("Defina SUPABASE_URL e SUPABASE_KEY no .env")

if not (ZAPI_INSTANCE and ZAPI_TOKEN and ZAPI_CLIENT_TOKEN):
    raise RuntimeError("Defina ZAPI_INSTANCE, ZAPI_TOKEN e ZAPI_CLIENT_TOKEN no .env")

ZAPI_BASE = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}"
SEND_TEXT_URL = f"{ZAPI_BASE}/send-text"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def send_text(phone: str, message: str):
    headers = {
        "Client-Token": ZAPI_CLIENT_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {"phone": phone, "message": message}
    resp = requests.post(SEND_TEXT_URL, headers=headers, json=payload, timeout=15)
    try:
        resp_json = resp.json()
    except Exception:
        resp.raise_for_status()
        resp_json = {}
    return resp.status_code, resp_json

def main():
    logging.info("Buscando contatos no Supabase...")
    contacts = fetch_contacts(limit=MAX_TO_SEND)
    if not contacts:
        logging.warning("Nenhum contato encontrado. Verifique a tabela 'contatos' no Supabase.")
        return

    sent = 0
    for c in contacts:
        name = c.get("nome") or "contato"
        raw_phone = c.get("telefone")
        phone = normalize_phone(raw_phone)
        if not phone:
            logging.warning(f"Contato {name} sem telefone válido. Pulando.")
            continue

        message = f"Olá {name}, tudo bem com você?"
        logging.info(f"Enviando para {phone} -> {message}")
        try:
            status, resp_json = send_text(phone, message)
            if status == 200:
                logging.info(f"Enviado com sucesso: {resp_json}")
            else:
                logging.error(f"Falha envio ({status}): {resp_json}")
        except Exception as e:
            logging.exception(f"Erro ao enviar para {phone}: {e}")

        sent += 1
        time.sleep(2)

    logging.info(f"Processo finalizado. Mensagens tentadas: {sent}")

if __name__ == "__main__":
    main()
