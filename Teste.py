import csv
import Unidade

# Nome do arquivo CSV
nome_arquivo = 'D:\\Teste_PNCP\\Arquivos_teste\\Unidades_csv.csv'

try:
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo_csv:
        # Criar um leitor CSV, especificando o delimitador como ';'
        leitor_csv = csv.reader(arquivo_csv, delimiter=';')
        contador = 0
        # Iterar sobre as linhas do arquivo
        for linha in leitor_csv:            
            nomeUnidade = linha[0]
            codigoUnidade = linha[1]
            if contador > 0:
                Unidade.inserirUnidade('21260443000191', codigoUnidade, nomeUnidade, '3133808')
                contador = contador + 1
            else:
                contador = contador + 1

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