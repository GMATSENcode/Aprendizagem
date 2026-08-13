import os
import mysql.connector
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def adicionar_lancamento(usuario_id, descricao, valor, tipo, data_lancamento):
    # 2. Resgata os valores das variáveis de ambiente
    host = os.getenv("DB_HOST", "127.0.0.1")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME", "planilha_db")
    port = int(os.getenv("DB_PORT", 3306))

    # 3. VERIFICAÇÃO DE SEGURANÇA: Checa se a senha foi lida do .env
    if not password:
        print(" AVISO: A variável 'DB_PASSWORD' não foi encontrada no arquivo .env!")
        print("Verifique se o arquivo .env está na mesma pasta do script e com o nome correto.")
        return

    try:
        # 4. Tenta abrir a conexão com o MySQL
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )

        cursor = conexao.cursor()

        # 5. Prepara a consulta SQL de inserção
        sql = """
        INSERT INTO lancamentos (usuario_id, descricao, valor, tipo, data_lancamento)
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (usuario_id, descricao, valor, tipo, data_lancamento)

        # 6. Executa a instrução e grava no banco
        cursor.execute(sql, valores)
        conexao.commit()

        print(f" Lançamento '{descricao}' de R$ {valor} inserido com sucesso!")

    except mysql.connector.Error as erro:
        print(f" Erro ao inserir lançamento no MySQL: {erro}")

    finally:
        # 7. Garante o fechamento dos recursos
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    # Teste de inserção para o usuário de ID 1
    adicionar_lancamento(
        usuario_id=1,
        descricao="Salário do Mês",
        valor=3000.00,
        tipo="RECEITA",
        data_lancamento="2026-08-01"
    )