import csv
import Unidade
import Usuario
from django.http import HttpResponse

# Nome do arquivo CSV
nome_arquivo = 'D:\\Teste_PNCP\\Arquivos_teste\\Unidades_csv8.csv'
lista_erros = []
listaEnteAutorizado = []
lista = []
cadastrarEnte = False
try:
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo_csv:
        # Criar um leitor CSV, especificando o delimitador como ';'
        leitor_csv = csv.reader(arquivo_csv, delimiter=';')
        contador = 0
        # Iterar sobre as linhas do arquivo
        cnpjOrgaoAnterior = 0
        
        for linha in leitor_csv:     
            cnpjOrgao = linha[0].replace('.','').replace('/','').replace('-','')         
            nomeUnidade = linha[2]
            codigoUnidade = linha[3]
            codigoIBGE = linha[4]
            
            if cnpjOrgao != '':
                if contador > 0:
                    contador = contador + 1
                    if cadastrarEnte:                    
                        if cnpjOrgaoAnterior != cnpjOrgao:
                            cnpjOrgaoAnterior = cnpjOrgao                    
                            listaEnteAutorizado.append(cnpjOrgao)                                                 
                            responseEntes = Usuario.inserirEnteAutorizado(listaEnteAutorizado, 0)
                            listaEnteAutorizado = []
                            if responseEntes.status_code != 200 and cnpjOrgao != '':
                                print(responseEntes.status_code)
                                print(cnpjOrgao)
                    
                   
                    response = Unidade.inserirUnidade(cnpjOrgao, codigoUnidade, nomeUnidade, codigoIBGE)
                   
                    if response.status_code != 201 and response.status_code != 200:
                        data = response.json()  # Converte o JSON em dicionário Python
                        mensagem = data.get("message")  # Pega o campo 'message'
                        if mensagem != "Código da unidade já cadastrado para o órgão.":
                            lista_erros.append(linha)   
                            lista_erros.append(mensagem)                                           
                    
                else:
                    contador = contador + 1
        
        if lista_erros != []:    
            for linha in lista_erros:
                print(linha)

except FileNotFoundError:
    print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

print("fim")


"""



import pandas as pd

# Nome do arquivo CSV
nome_arquivo = 'D:\\Teste_PNCP\\Arquivos_teste\\Unidades_csv.csv'

try:
    # Ler o arquivo CSV, especificando o separador como ';'
    df = pd.read_csv(nome_arquivo, sep=';')

    # Exibir as primeiras 5 linhas do DataFrame para verificar se a leitura foi correta
    leitor_csv = df.head()
    for linha in leitor_csv:
            print(linha)
    


except FileNotFoundError:
    print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

print('fim linha')"""