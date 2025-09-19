import csv
import Unidade
import Usuario

# Nome do arquivo CSV
nome_arquivo = 'D:\\Teste_PNCP\\Arquivos_teste\\Unidades_csv8.csv'
lista_erros = []
listaEnteAutorizado = []
lista = []
try:
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo_csv:
        # Criar um leitor CSV, especificando o delimitador como ';'
        leitor_csv = csv.reader(arquivo_csv, delimiter=';')
        contador = 0
        # Iterar sobre as linhas do arquivo
        cnpjOrgaoAnterior = 0
        
        for linha in leitor_csv:     
            cnpjOrgao = linha[8]       
            nomeUnidade = linha[2]
            codigoUnidade = linha[3]
            codigoIBGE = linha[4]
            
            if contador > 0:
                contador = contador + 1
                if cnpjOrgaoAnterior != cnpjOrgao:
                    cnpjOrgaoAnterior = cnpjOrgao
                    listaEnteAutorizado.append(cnpjOrgao)
                
                response = Unidade.inserirUnidade(cnpjOrgao, codigoUnidade, nomeUnidade, codigoIBGE)
                if response.status_code != 201:
                    lista_erros.append(linha)                        
                    
            else:
                contador = contador + 1
        responseEntes = Usuario.inserirEnteAutorizado(listaEnteAutorizado, 5)
        if lista != []:    
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