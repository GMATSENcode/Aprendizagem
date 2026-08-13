import os
import mysql.connector
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

try:
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "planilha_db"),
        port=int(os.getenv("DB_PORT", 3306))  # Converte para int e define 3306 como padrão
    )

    if conexao.is_connected():
        print(" Conexão com o MySQL realizada com sucesso!")
        conexao.close()

except Exception as e:
    print(f" Erro ao conectar ao banco de dados: {e}")