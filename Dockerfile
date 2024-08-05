# Utilizando a imagem base oficial do Python
FROM python:3.8

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando o arquivo de requisitos e instalando dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiando o restante do código da aplicação
COPY . .

# Expondo a porta 8000
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "project:app", "--host", "0.0.0.0", "--port", "8000"]
