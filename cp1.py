# 1TDCPG Henrique
# Alvo https://www2.fiap.com.br

import requests
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Verificar subdomínios e paths/arquivos de um URL alvo.")
    parser.add_argument("url", help="A URL alvo para verificar subdomínios e paths.", nargs="?")
    args = parser.parse_args()

    if not args.url:
        print("Erro: A URL alvo deve ser fornecida.")
        print("Uso: python cp1.py <URL alvo>")
        sys.exit(1)

    base_url = args.url
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        print("Erro: A URL alvo deve começar com 'http://' ou 'https://'.")
        sys.exit(1)

    domain = base_url.split("://")[-1]  # Remove o esquema (http:// ou https://) para obter o domínio

    subdomain_list = enumerate_subdomains(domain)
    if subdomain_list:
        print (f"Subdomínios encontrados com status 200: {subdomain_list}")
    else:
        print("Nenhum subdomínio com status 200 encontrado.")
    
    wordlist_paths = [line.strip() for line in open('common.txt', 'r')]
    wordlist_files = [line.strip() for line in open('common.txt', 'r')]

    paths_status, files_status = enumerate_paths(base_url, wordlist_paths, wordlist_files)
    display_results(paths_status, files_status)

def check_status(url):
    try:
        response = requests.get(url, timeout=5)  # Adiciona um timeout para evitar que o código trave
        return response.status_code
    except requests.RequestException:
        return None  # Retorna None em caso de erro

def normalize_url(base_url, path):
    if base_url.endswith('/'):
        base_url = base_url.rstrip('/')
    if path.startswith('/'):
        path = path.lstrip('/')
    return f"{base_url}/{path}"

def enumerate_paths(base_url, wordlist_paths, wordlist_files):
    paths_status = {}
    files_status = {}

    print("Verificando paths...")
    for path in wordlist_paths:
        url = normalize_url(base_url, path)
        status_code = check_status(url)
        if status_code is not None:
            paths_status[url] = status_code

    print("Verificando arquivos...")
    for file in wordlist_files:
        url = normalize_url(base_url, file)
        status_code = check_status(url)
        if status_code is not None:
            files_status[url] = status_code

    return paths_status, files_status

def filter_files(files_status, allowed_extensions):
    filtered_files = {}
    for url, status_code in files_status.items():
        if any(url.lower().endswith(ext) for ext in allowed_extensions):
            filtered_files[url] = status_code
    return filtered_files

def display_results(paths_status, files_status):
    allowed_extensions = ['.doc', '.docx', '.pdf', '.txt', '.rtf', '.odt', '.html', '.htm', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.svg', '.mp3', '.wav', '.flac', '.aac', '.ogg', '.mp4', '.avi', '.mov', '.mkv', '.webm', '.exe', '.app', '.bat', '.sh', '.jar', '.csv', '.xml', '.json', '.sql', '.zip', '.rar', '.7z', '.tar', '.gz', '.py', '.js', '.java', '.css', '.php', '.cpp', '.c', '.db', '.sqlite', '.mdb', '.accdb', '.iso', '.img', '.bak', '.ini', '.conf', '.cfg', '.sys', '.ttf', '.otf', '.fon', '.docm', '.wps', '.pages', '.raw', '.heic', '.heif', '.ico', '.wma', '.au', '.m4a', '.3gp', '.flv', '.mts', '.msi', '.appx', '.run', '.bz2', '.lz', '.z', '.rb', '.pl', '.swift', '.lua', '.jsonl', '.dbf', '.prn', '.dmg', '.vhd', '.vhdx', '.log', '.plist', '.yaml', '.yml', '.pfb', '.afm', '.epub', '.mobi', '.ics', '.md', '.tex']
    filtered_files = filter_files(files_status, allowed_extensions)
    
    # Exibindo paths com status 200
    print("\nPaths encontrados com status 200:")
    for url, status_code in paths_status.items():
        if status_code == 200:
            print(url)

    # Exibindo arquivos com status 200
    print("\nArquivos encontrados com status 200:")
    for url, status_code in filtered_files.items():
        if status_code == 200:
            print(url)

def enumerate_subdomains(domain):
    subdomains = []
    common_subdomains = ['www', 'mail', 'ftp', 'blog', 'shop', 'admin']

    print("Verificando subdomínios...")
    for sub in common_subdomains:
        subdomain = f"http://{sub}.{domain}"
        status_code = check_status(subdomain)
        if status_code == 200:
            subdomains.append(subdomain)
    
    return subdomains

if __name__ == "__main__":
    main()
