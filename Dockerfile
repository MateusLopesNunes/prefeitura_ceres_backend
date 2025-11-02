# Use a imagem base do Python
FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Atualiza o pip
RUN pip install --upgrade pip

# Copia o arquivo de dependências e instala
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copia o código do projeto
COPY cbc/ ./cbc

# Adiciona o script wait-for-it.sh
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Define o diretório de trabalho para a aplicação Django
WORKDIR /app/cbc