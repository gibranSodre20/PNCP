import requests
from typing import Optional, Dict, Any, Union

BASE_URL = "https://treina.pncp.gov.br/api/pncp"

response = None

def executa_endpoint(endpoint, json_data, headers, files, possuiArquivos):
    #Add commentMore actions
    url_endpoint= f"{BASE_URL}" + endpoint   
    if possuiArquivos:
        response = requests.post(url_endpoint, headers=headers, files=files, verify=False)#data=json_data, verify=False)  # verify=False ignora o SSL
    else:
        response = requests.post(url_endpoint, headers=headers, data=json_data, verify=False)  # verify=False ignora o SSL

    return response