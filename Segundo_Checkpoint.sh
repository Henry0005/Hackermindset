#!/bin/bash

# Função para obter o título da página
get_title() {
    wget -qO- --no-check-certificate "$1" | grep -oPi '<title[^>]*>(?:(?!<\/title>).)*<\/title>' | perl -pe 's/<title[^>]*>((?:(?!<\/title>).)*)<\/title>/\1/i'
}

# Função para obter o servidor web
get_server() {
    curl -sI "$1" | grep -i 'Server:' | awk '{print $2}'
}

# Função para obter a linguagem de programação
get_language() {
    # Verifica se o conteúdo retornado é HTML
    html=$(curl -s "$1")
    grep -q '<html' <<< "$html" || { echo "O site não parece estar retornando conteúdo HTML"; return; }

    # Verifica se o site utiliza PHP
    curl -sI "$1" | grep -q 'X-Powered-By: PHP' && { echo "PHP"; return; }

    # Verifica se o site utiliza Python
    curl -sI "$1" | grep -q 'X-Powered-By: ASP.NET' && { echo "ASP.NET"; return; }

    # Verifica se o site utiliza JavaScript (com jQuery)
    if grep -q '<script src="[^"]+jquery\.js">' <<< "$html"; then
        echo "JavaScript (com jQuery)"; return;
    fi

    # Verifica se o site utiliza Ruby on Rails
    if grep -q '<%= csrf_meta_tag %>' <<< "$html"; then
        echo "Ruby on Rails"; return;
    fi

    # Verifica se o site utiliza Python (Django)
    if grep -q 'django\.html' <<< "$html"; then
        echo "Python (Django)"; return;
    fi

    # Verifica se o site utiliza Java
    if grep -q '<jsp:useBean id="app" class="com.example.App" />' <<< "$html"; then
        echo "Java"; return;
    fi

    # Verifica se o site utiliza C# (ASP.NET MVC)
    if grep -q '<system.webmvc controllertype="MyController" action="Index">' <<< "$html"; then
        echo "C# (ASP.NET MVC)"; return;
    fi

    # Adicione mais verificações para outras linguagens, se necessário

    # Se nenhuma linguagem específica for encontrada, retorna "Não foi possível determinar"
    echo "Não foi possível determinar a linguagem de programação"
}

# Função para extrair URLs do website
extract_urls() {
    wget -qO- --no-check-certificate "$1" | grep -oE 'href="([^"#]+)"' | sed 's/href="\(.*\)"/\1/'
}

## Função para extrair todos os formulários e inputs de texto do website
extract_forms() {
    wget -qO- --no-check-certificate "$1" | python3 -c '
from bs4 import BeautifulSoup
import sys

html = sys.stdin.read()
soup = BeautifulSoup(html, "html.parser")
forms = soup.find_all("form")

for form in forms:
    inputs = form.find_all("input", {"type": "text"})
    for input_tag in inputs:
        print(input_tag.get("name", ""))
'
}

# Verifica se o argumento foi fornecido
if [ $# -ne 1 ]; then
    echo "Uso: $0 <URL>"
    exit 1
fi

url="$1"

# Obtém e exibe o título da página
title=$(get_title "$url")
echo "Título da página: $title"

# Obtém e exibe o servidor web
server=$(get_server "$url")
echo "Servidor web: $server"

# Obtém e exibe a linguagem de programação (se disponível)
language=$(get_language "$url")
echo "Linguagem de programação: $language"

# Extrai e exibe as URLs do website
echo "URLs encontradas:"
extract_urls "$url"

# Extrai e exibe todos os formulários e inputs de texto do website
echo "Formulários e inputs de texto encontrados:"
extract_forms "$url"
