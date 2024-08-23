import requests

def check_status(url):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return None

def normalize_url(base_url, path):
    """
    Normaliza a URL base e o path para evitar barras duplicadas.
    
    :param base_url: URL base do site.
    :param path: Caminho a ser concatenado com a URL base.
    :return: URL normalizada.
    """
    if base_url.endswith('/'):
        base_url = base_url.rstrip('/')
    if path.startswith('/'):
        path = path.lstrip('/')
    return f"{base_url}/{path}"

def enumerate_paths(base_url, wordlist_paths, wordlist_files):
    """
    Enumera paths e arquivos no site com base nas wordlists fornecidas.
    
    :param base_url: URL base do site a ser explorado.
    :param wordlist_paths: Lista de paths para verificar.
    :param wordlist_files: Lista de arquivos para verificar.
    :return: Dois dicionários com URLs e códigos de status.
    """
    paths_status = {}
    files_status = {}

    # Enumerando paths
    print("Verificando paths...")
    for path in wordlist_paths:
        url = normalize_url(base_url, path)
        status_code = check_status(url)
        paths_status[url] = status_code

    # Enumerando arquivos
    print("Verificando arquivos...")
    for file in wordlist_files:
        url = normalize_url(base_url, file)
        status_code = check_status(url)
        files_status[url] = status_code

    return paths_status, files_status

def filter_files(files_status, allowed_extensions):
    """
    Filtra arquivos com base nas extensões permitidas.
    
    :param files_status: Dicionário com URLs e códigos de status dos arquivos.
    :param allowed_extensions: Lista de extensões permitidas.
    :return: Dicionário com URLs e códigos de status dos arquivos filtrados.
    """
    filtered_files = {}
    for url, status_code in files_status.items():
        if any(url.lower().endswith(ext) for ext in allowed_extensions):
            filtered_files[url] = status_code
    return filtered_files

def display_results(paths_status, files_status):
    """
    Exibe os resultados das verificações de status, paths e arquivos encontrados.
    
    :param paths_status: Dicionário com URLs e códigos de status dos paths.
    :param files_status: Dicionário com URLs e códigos de status dos arquivos.
    """
    # Exibindo status codes
    print("\nStatus Code:")
    all_status = {**paths_status, **files_status}
    for url, status_code in all_status.items():
        print(f"{url} - Status: {status_code}")

    # Exibindo paths encontrados
    print("\nPaths encontrados:")
    for url, status_code in paths_status.items():
        if status_code == 200:
            print(url)

    # Exibindo arquivos encontrados com extensões
    allowed_extensions = ['.doc', '.docx', '.pdf', '.txt', '.rtf', '.odt', '.html', '.htm', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.svg', '.mp3', '.wav', '.flac', '.aac', '.ogg', '.mp4', '.avi', '.mov', '.mkv', '.webm', '.exe', '.app', '.bat', '.sh', '.jar', '.csv', '.xml', '.json', '.sql', '.zip', '.rar', '.7z', '.tar', '.gz', '.py', '.js', '.java', '.css', '.php', '.cpp', '.c', '.db', '.sqlite', '.mdb', '.accdb', '.iso', '.img', '.bak', '.ini', '.conf', '.cfg', '.sys', '.ttf', '.otf', '.fon', '.docm', '.wps', '.pages', '.raw', '.heic', '.heif', '.ico', '.wma', '.au', '.m4a', '.3gp', '.flv', '.mts', '.msi', '.appx', '.run', '.bz2', '.lz', '.z', '.rb', '.pl', '.swift', '.lua', '.jsonl', '.dbf', '.prn', '.dmg', '.vhd', '.vhdx', '.log', '.plist', '.yaml', '.yml', '.pfb', '.afm', '.epub', '.mobi', '.ics', '.md', '.tex']
    filtered_files = filter_files(files_status, allowed_extensions)
    
    print("\nArquivos encontrados:")
    for url, status_code in filtered_files.items():
        if status_code == 200:
            print(url)

if __name__ == "__main__":
    base_url = input("Digite a URL alvo (exemplo: https://example.com): ").strip()

    # Carregar wordlists, se desejar utilizar outras Wordlists alterar os arquivos .txt
    wordlist_paths = [line.strip() for line in open('common.txt', 'r')]
    wordlist_files = [line.strip() for line in open('common.txt', 'r')]

    paths_status, files_status = enumerate_paths(base_url, wordlist_paths, wordlist_files)
    display_results(paths_status, files_status)
