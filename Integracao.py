import requests
from typing import Optional, Dict, Any, Union

BASE_URL = "https://pncp.gov.br/api/pncp"

def executa_endpoint(endpoint, json_data, headers, files, possuiArquivos, atualizacao, consulta):
    #Add commentMore actions
    url_endpoint= f"{BASE_URL}" + endpoint   
    if consulta:
        response = requests.get(url_endpoint, headers=headers, files=files, verify=False)
    else:
        if possuiArquivos:
            response = requests.post(url_endpoint, headers=headers, files=files, verify=False)#data=json_data, verify=False)  # verify=False ignora o SSL
        else:
            if atualizacao:
                response = requests.put(url_endpoint, headers=headers, data=json_data, verify=False) 
            else:    
                response = requests.post(url_endpoint, headers=headers, data=json_data, verify=False) 
     # verify=False ignora o SSL

    return response