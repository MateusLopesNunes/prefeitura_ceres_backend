# Use a imagem base do Python
FROM python:3.8.10

# Define o diretório de trabalho dentro do container
WORKDIR /app

RUN pip install --upgrade pip

RUN pip install Django

# Copia o arquivo requirements.txt e instala as dependências
COPY requeriments.txt .

# Instala as dependências do projeto
RUN pip install -r requeriments.txt

# Copia o restante do código para o diretório de trabalho
COPY cbc/ ./cbc  
# Copia a aplicação para dentro do diretório de trabalho

# Define o diretório de trabalho para a aplicação Django
WORKDIR /app/cbc 
# Muda para o diretório da aplicação Django
