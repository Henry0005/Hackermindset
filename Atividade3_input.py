# Nome do arquivo a ser lido
nome_arquivo = "darkweb2017-top100.txt"

# Solicita ao usuário a quantidade de linhas a serem lidas no arquivo alvo
try:
    num_linhas = int(input("Digite o número de linhas a serem lidas do arquivo alvo: "))
except ValueError:
    print("Por favor, insira um número válido.")
    exit(1)  # Encerra o script se a entrada não for um número válido

# Tenta abrir e ler o arquivo
try:
    with open(nome_arquivo, 'r') as arquivo:
        # Lê o número especificado de linhas
        for i, linha in enumerate(arquivo):
            if i < num_linhas:
                print(linha, end='')
            else:
                break
except FileNotFoundError:
    print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
except IOError:
    print(f"Ocorreu um erro ao tentar ler o arquivo '{nome_arquivo}'.")
