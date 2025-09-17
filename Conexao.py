import requests
from dotenv import load_dotenv
import os
import datetime

# Carrega variáveis do arquivo .env
load_dotenv()

# Base URL da API
BASE_URL = 'https://pncp.gov.br/api/pncp'

# Acessa as variáveis de ambiente
LOGIN = os.getenv("login")
SENHA = os.getenv("senhaSwagger")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# Armazenamento do token e expiração
TOKEN = None
EXPIRATION_TIME = None


def is_token_valid() -> bool:
    """Verifica se o token ainda está válido"""
    global TOKEN, EXPIRATION_TIME
    if TOKEN and EXPIRATION_TIME:
        return datetime.datetime.now() < EXPIRATION_TIME
    return False


def get_token() -> str | None:
    """Retorna o token atual ou gera um novo se necessário"""
    global TOKEN, EXPIRATION_TIME

    if is_token_valid():
        if DEBUG_MODE:
            print("[DEBUG] Token ainda válido, reutilizando.")
        return TOKEN

    if not LOGIN or not SENHA:
        if DEBUG_MODE:
            print("[ERRO] Variáveis de ambiente 'login' ou 'senhaSwagger' não estão definidas.")
        return None

    url = f"{BASE_URL}/v1/usuarios/login"
    dados = {"login": LOGIN, "senha": SENHA}

    try:
        resposta = requests.post(url, json=dados)
        resposta.raise_for_status()  # Lança exceção para códigos de erro HTTP

        token = resposta.headers.get("Authorization")
        if token:
            TOKEN = token
            EXPIRATION_TIME = datetime.datetime.now() + datetime.timedelta(hours=1)
            if DEBUG_MODE:
                print("[DEBUG] Novo token obtido com sucesso. Expira em:", EXPIRATION_TIME)
        else:
            if DEBUG_MODE:
                print("[ERRO] Nenhum token retornado no cabeçalho.")

        return TOKEN

    except requests.exceptions.RequestException as e:
        if DEBUG_MODE:
            print(f"[ERRO] Falha na requisição: {e}")
        return None