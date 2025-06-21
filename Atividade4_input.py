import requests

def verificar_subdominios(url, wordlist_path="subdomains-top1million-5000.txt"):
    # Solicita ao usuário o número de subdomínios a serem verificados no URL alvo
    try:
        num_subdominios = int(input("Digite o número de subdomínios a serem verificados: "))
    except ValueError:
        print("Por favor, insira um número válido.")
        return
    
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

url_alvo = input("Digite o URL do alvo: ")
verificar_subdominios(url_alvo)
