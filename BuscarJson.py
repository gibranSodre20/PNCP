import requests
import json
import os


def buscar_json_raw(nome_json):
    try:
        base_dir = os.path.dirname(__file__)
        caminho_json = os.path.join(base_dir, 'Arquivos_Json', nome_json)

        with open(caminho_json, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
        return dados

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_json}' não foi encontrado em {caminho_json}.")
        return None
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar o JSON: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def buscar_documento_raw(url_documento):
    
    response = requests.get(url_documento)

    if response.status_code == 200:
        with open("arquivo_baixado.pdf", "wb") as f:
            f.write(response.content)
            print(type(f))
            return f.BytesIO()
        print("Arquivo PDF salvo com sucesso!")
    else:
        print(f"Erro ao baixar o arquivo: {response.status_code}")
    
  