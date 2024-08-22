import requests
import argparse
import sys

def verificar_subdominios(url, wordlist_path="subdomains-top1million-5000.txt", num_subdominios=20):
    try:
        with open(wordlist_path, 'r') as arquivo:
            subdominios = [linha.strip() for linha in arquivo.readlines()]
        subdominios = subdominios[:num_subdominios]
        for subdominio in subdominios:
            subdominio_url = f"http://{subdominio}.{url}"
            try:
                resposta = requests.get(subdominio_url)
                print(f"{subdominio_url} - Status Code: {resposta.status_code}")
            except requests.RequestException as e:
                print(f"Erro ao acessar {subdominio_url}: {e}")
    
    except FileNotFoundError:
        print(f"O arquivo '{wordlist_path}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def main():
    parser = argparse.ArgumentParser(description="Verificar subdomínios de um URL alvo.")
    parser.add_argument("url", nargs="?", help="A URL alvo para verificar subdomínios.")
    args = parser.parse_args()
    
    if not args.url:
        print("Erro: A URL alvo deve ser fornecida.")
        print("Uso: python Atividade4_argument.py <URL>")
        sys.exit(1) 
    
    url_alvo = args.url
    verificar_subdominios(url_alvo)

if __name__ == "__main__":
    main()
