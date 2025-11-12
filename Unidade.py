import Integracao
import json
import Conexao
import BuscarJson
import os
import csv
import Usuario
from datetime import datetime
from dateutil.relativedelta import relativedelta

json_data = None
#token = Conexao.get_token()
files = None
endpoint = None

#cnpj = "17572121000100" #os.getenv ("cnpj_treinamento")
usuario_git = os.getenv ("usuario_git")
repositorio = os.getenv ("repositorio")
#lista_erros = []

def cadastarEntesUnidades(id_usuario, arquivo_csv, cadastrar_ente, cadastrar_unidade, login, senha):
        
        try:    
            totalUnidadeCadastrada = 0
            totalEntesAutorizadosCadastrados = 0
            caminhoArquivoCsv = arquivo_csv.replace('/', '\\')
            lista_erros = []
            listaEnteAutorizado = []      
            with open(caminhoArquivoCsv, 'r', newline='', encoding='utf-8') as arquivo:
                leitor_csv = csv.reader(arquivo, delimiter=';')
                contador = 0
                # Iterar sobre as linhas do arquivo
                cnpjOrgaoAnterior = 0
            
                for linha in leitor_csv:     
                    cnpjOrgao = linha[0].replace('.','').replace('/','').replace('-','')       
                    nomeUnidade = linha[1]
                    codigoUnidade = linha[2]
                    codigoIBGE = linha[3]
                    
                    if cnpjOrgao != '':
                        if contador > 0:
                            contador = contador + 1
                            if cadastrar_ente:                    
                                if cnpjOrgaoAnterior != cnpjOrgao:
                                    cnpjOrgaoAnterior = cnpjOrgao                    
                                    listaEnteAutorizado.append(cnpjOrgao)        
                                    
                                    #Verifica se o órgão já está cadastrado
                                    if not Usuario.consultarEnteAutorizado(id_usuario, cnpjOrgao, login, senha):                                                                                                                      
                                        responseEntes = Usuario.inserirEnteAutorizado(listaEnteAutorizado, id_usuario, login, senha)
                                        listaEnteAutorizado = []
                                        if responseEntes.status_code != 200 and cnpjOrgao != '':
                                            data = responseEntes.json()  # Converte o JSON em dicionário Python
                                            mensagem = data.get("message")  # Pega o campo 'message'
                                            lista_erros.append(cnpjOrgao)   
                                            lista_erros.append(mensagem)
                                        else:
                                            totalEntesAutorizadosCadastrados = totalEntesAutorizadosCadastrados + 1                            
                        
                            responseUnidade = inserirUnidade(cnpjOrgao, codigoUnidade, nomeUnidade, codigoIBGE, login, senha)
                        
                            if responseUnidade.status_code != 201 and responseUnidade.status_code != 200:
                                data = responseUnidade.json()  # Converte o JSON em dicionário Python
                                mensagem = data.get("message")  # Pega o campo 'message'
                                if mensagem != "Código da unidade já cadastrado para o órgão.":
                                    lista_erros.append(linha)   
                                    lista_erros.append(mensagem)
                            else:
                                totalUnidadeCadastrada = totalUnidadeCadastrada + 1                                                                               
                            
                        else:
                            contador = contador + 1
                            
            if lista_erros == []:
               lista_erros.append("A execução ocorreu sem erros." )
                 
            lista_erros.append(f"Total de entes cadastrados = {totalEntesAutorizadosCadastrados}" )
            lista_erros.append(f"Total de unidades cadastradas = {totalUnidadeCadastrada}" )
            
            return lista_erros

        except FileNotFoundError:
            print(f"Erro: O arquivo '{caminhoArquivoCsv}' não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
       

def inserirUnidade(cnpj, codigoUnidade, nomeUnidade, codigoIBGE, login, senha):
    token = Conexao.get_token(login, senha)
    endpoint = f"/v1/orgaos/{cnpj}/unidades"

    #url_json = f"https://raw.githubusercontent.com/{usuario_git}/{repositorio}/refs/heads/main/Arquivos_Json/InserirUnidade.json"
    #json_unidade = BuscarJson.buscar_json_raw(url_json)
    #base_dir = os.path.dirname(__file__)
    json_unidade = BuscarJson.buscar_json_raw("InserirUnidade.json") #os.path.join(base_dir, 'Arquivos_Json', 'InserirUnidade.json') #'D:\\Teste_PNCP\\Arquivos_Json\\InserirUnidade.json'
    # Abre o arquivo JSON
    #with open(json_unidade, 'r', encoding='utf-8') as arquivo:
    #    json_unidade = json.load(arquivo)
    
    json_unidade["codigoIBGE"] = codigoIBGE
    json_unidade["codigoUnidade"] = codigoUnidade 
    json_unidade["nomeUnidade"] = nomeUnidade 
    #json_unidade = json.dumps(json_unidade, ensure_ascii=False)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "*/*",
        "Content-Type": "application/json"
        }
    response = Integracao.executa_endpoint(endpoint, json.dumps(json_unidade, indent=4), headers, files, False, False, False)
    return response

def atualizarUnidade(cnpj, codigoUnidade, nomeUnidade, codigoIBGE, login, senha):
    token = Conexao.get_token(login, senha)
    endpoint = f"/v1/orgaos/{cnpj}/unidades"

    url_json = f"https://raw.githubusercontent.com/{usuario_git}/{repositorio}/refs/heads/main/Arquivos_Json/InserirUnidade.json"
    json_unidade = BuscarJson.buscar_json_raw(url_json)
    json_unidade["codigoIBGE"] = codigoIBGE
    json_unidade["codigoUnidade"] = codigoUnidade 
    json_unidade["nomeUnidade"] = nomeUnidade 
    #json_unidade = json.dumps(json_unidade, ensure_ascii=False)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "*/*",
        "Content-Type": "application/json"
        }
    response = Integracao.executa_endpoint(endpoint, json.dumps(json_unidade, indent=4), headers, files, False, True)
    return response