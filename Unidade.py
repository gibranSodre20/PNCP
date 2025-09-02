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

cnpj = "21260443000191" #os.getenv ("cnpj_treinamento")
usuario_git = os.getenv ("usuario_git")
repositorio = os.getenv ("repositorio")

def inserirUnidade(cnpj, codigoUnidade, nomeUnidade, codigoIBGE):
    endpoint = f"/v1/orgaos/{cnpj}/unidades"

    url_json = f"https://raw.githubusercontent.com/{usuario_git}/{repositorio}/refs/heads/main/Arquivos_Json/InserirUnidade.json"
    json_unidade = BuscarJson.buscar_json_raw(url_json)
    json_unidade["codigoIBGE"] = codigoIBGE
    json_unidade["codigoUnidade"] = codigoUnidade 
    json_unidade["nomeUnidade"] = nomeUnidade 
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "*/*",
        "Content-Type": "application/json"
        }
    response = Integracao.executa_endpoint(endpoint, json.dumps(json_unidade, indent=4), headers, files, False)
    print(response)