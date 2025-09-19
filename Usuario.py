import Integracao
import json
import Conexao
import BuscarJson
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

json_data = None
token = Conexao.get_token()
files = None
endpoint = None

#cnpj = "17572121000100" #os.getenv ("cnpj_treinamento")
usuario_git = os.getenv ("usuario_git")
repositorio = os.getenv ("repositorio")

def inserirEnteAutorizado(lista_cnpj, codigoUsuario):
    endpoint = f"/v1/usuarios/{codigoUsuario}/orgaos"

    url_json = f"https://raw.githubusercontent.com/{usuario_git}/{repositorio}/refs/heads/main/Arquivos_Json/InserirEnteAutorizado.json"
    json_EnteAutorizado = BuscarJson.buscar_json_raw(url_json)
    json_EnteAutorizado["entesAutorizados"] = lista_cnpj
    
    #json_unidade = json.dumps(json_unidade, ensure_ascii=False)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "*/*",
        "Content-Type": "application/json"
        }
    response = Integracao.executa_endpoint(endpoint, json.dumps(json_EnteAutorizado, indent=4), headers, files, False)
    return response