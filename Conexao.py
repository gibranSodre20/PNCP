import requests
from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()

# Base URL da API
BASE_URL = 'https://treina.pncp.gov.br/api/pncp'

# Acessa as variáveis de ambiente
LOGIN = os.getenv("login")
SENHA = os.getenv("senhaSwagger")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

def get_token() -> str | None:
  
    if not LOGIN or not SENHA:
        if DEBUG_MODE:
            print("[ERRO] Variáveis de ambiente 'login' ou 'senhaSwagger' não estão definidas.")
        return None

    url = f"{BASE_URL}/v1/usuarios/login"
    dados = {
        "login": LOGIN,
        "senha": SENHA
    }

    try:
        resposta = requests.post(url, json=dados)
        resposta.raise_for_status()  # Lança exceção para códigos de erro HTTP

        token = resposta.headers.get("Authorization")
        if token and DEBUG_MODE:
            print("[DEBUG] Token obtido com sucesso.")

        return token
    except requests.exceptions.RequestException as e:
        if DEBUG_MODE:
            print(f"[ERRO] Falha na requisição: {e}")
        return None