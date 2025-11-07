import Integracao
import json
import Conexao
import BuscarJson
import os
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

json_data = None
token = None #Conexao.get_token(login, senha)
files = None
endpoint = None

#cnpj = "17572121000100" #os.getenv ("cnpj_treinamento")
usuario_git = os.getenv ("usuario_git")
repositorio = os.getenv ("repositorio")

def consultarEnteAutorizado(codigoUsuario, cnpjEnte, login, senha):
    token = Conexao.get_token(login, senha)
    endpoint = f"/v1/usuarios/{codigoUsuario}"
    
    headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
            }
    response = Integracao.executa_endpoint(endpoint, None, headers, files, False, False, True)
    
    if response.status_code == 200:
       # Adiciona os CNPJs dos entes autorizados
       dados = response.json()
       
        # Adiciona os CNPJs dos entes autorizados
    if 'entesAutorizados' in dados:
        # Inicializa a lista de CNPJs
        cnpjs = []
        cnpjs += [ente['cnpj'] for ente in dados['entesAutorizados'] if 'cnpj' in ente]
        
    return cnpjEnte in cnpjs
        
        
def consultarUsuario(codigoUsuario, arquivo_csv, login, senha):
    token = Conexao.get_token(login, senha)
    endpoint = f"/v1/usuarios/{codigoUsuario}"
    ListaCnpjsOrgaosNaoCadastrados = []
    #base_dir = os.path.dirname(__file__)
    #json_EnteAutorizado = BuscarJson.buscar_json_raw(os.path.join(base_dir, 'Arquivos_Json', 'InserirUnidade.json'))
    headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
            }
    
    response = Integracao.executa_endpoint(endpoint, None, headers, files, False, False, True)
    
    if response.status_code == 200:
       # Adiciona os CNPJs dos entes autorizados
       dados = response.json()
       
        # Adiciona os CNPJs dos entes autorizados
    if 'entesAutorizados' in dados:
         # Inicializa a lista de CNPJs
        cnpjs = []
        cnpjs += [ente['cnpj'] for ente in dados['entesAutorizados'] if 'cnpj' in ente]
        
    # Exibe os resultados (um por linha, entre aspas duplas)
    #for cnpj in cnpjs:
        try:
        
            caminhoArquivoCsv = arquivo_csv.replace('/', '\\')
        
            with open(caminhoArquivoCsv, 'r', newline='', encoding='utf-8') as arquivo:
                leitor_csv = csv.reader(arquivo, delimiter=';')
                contador = 0
                # Iterar sobre as linhas do arquivo
                cnpjOrgaoAnterior = 0
                                
                for linha in leitor_csv:  
                    if contador > 0:
                        cnpjOrgao = linha[0].replace('.','').replace('/','').replace('-','')
                        
                        if cnpjOrgaoAnterior != cnpjOrgao:
                            cnpjOrgaoAnterior = cnpjOrgao
                            if cnpjOrgao not in cnpjs and cnpjOrgao != '':
                                ListaCnpjsOrgaosNaoCadastrados.append(cnpjOrgao)
                                contador = contador + 1
                            else:
                                contador = contador + 1
                    else:
                        contador = contador + 1   
                       
            if ListaCnpjsOrgaosNaoCadastrados == []:
                ListaCnpjsOrgaosNaoCadastrados.append("Todos os entes públicos já estavam cadastrados.")
                        
        except FileNotFoundError:
            print(f"Erro: O arquivo '{arquivo_csv}' não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            
          
    return ListaCnpjsOrgaosNaoCadastrados
    

def inserirEnteAutorizado(cnpj, codigoUsuario, login, senha):
    endpoint = f"/v1/usuarios/{codigoUsuario}/orgaos"
    token = Conexao.get_token(login, senha)

    #base_dir = os.path.dirname(__file__)
    #json_unidade = os.path.join(base_dir, 'Arquivos_Json', 'InserirUnidade.json')
    #url_json = f"https://raw.githubusercontent.com/{usuario_git}/{repositorio}/refs/heads/main/Arquivos_Json/InserirEnteAutorizado.json"
    json_EnteAutorizado = BuscarJson.buscar_json_raw("InserirEnteAutorizado.json")
    json_EnteAutorizado["entesAutorizados"] = cnpj
    
    #json_unidade = json.dumps(json_unidade, ensure_ascii=False)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "*/*",
        "Content-Type": "application/json"
        }
    
    response = Integracao.executa_endpoint(endpoint, json.dumps(json_EnteAutorizado, indent=4), headers, files, False, False, False)
   
    return response
    