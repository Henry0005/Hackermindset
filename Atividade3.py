# Nome do arquivo a ser lido
nome_arquivo = "darkweb2017-top100.txt"

# Tenta abrir e ler o arquivo alvo
try:
    with open(nome_arquivo, 'r') as arquivo:
        # Lê somente as 10 primeiras linhas
        for i, linha in enumerate(arquivo):
            if i < 10:
                print(linha, end='')
            else:
                break
except FileNotFoundError:
    print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
except IOError:
    print(f"Ocorreu um erro ao tentar ler o arquivo '{nome_arquivo}'.")
