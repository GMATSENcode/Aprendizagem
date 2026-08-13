import os
import mysql.connector
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

def resolver_e_inserir():
    # 2. Resgata e valida as credenciais
    host = os.getenv("DB_HOST", "127.0.0.1")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME", "planilha_db")
    port = int(os.getenv("DB_PORT", 3306))

    if not password:
        print(" Erro: 'DB_PASSWORD' não encontrada no arquivo .env!")
        return

    try:
        # 3. Conecta ao MySQL
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )

        cursor = conexao.cursor()

        # --- PASSO 1: Garantir que o Usuário existe ---
        print("Passo 1: Verificando/Cadastrando usuário...")
        
        sql_usuario = """
        INSERT INTO usuarios (id, nome, email) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE nome=VALUES(nome);
        """
        dados_usuario = (1, "Nick", "nick@email.com")
        
        cursor.execute(sql_usuario, dados_usuario)
        conexao.commit()
        print(" Usuário de ID 1 garantido com sucesso!")

        # --- PASSO 2: Inserir o Lançamento vinculado ao ID 1 ---
        print("\nPasso 2: Inserindo lançamento financeiro...")
        
        sql_lancamento = """
        INSERT INTO lancamentos (usuario_id, descricao, valor, tipo, data_lancamento)
        VALUES (%s, %s, %s, %s, %s);
        """
        dados_lancamento = (1, "Salário do Mês", 3000.00, "RECEITA", "2026-08-01")
        
        cursor.execute(sql_lancamento, dados_lancamento)
        conexao.commit()
        print(" Lançamento financeiro inserido com sucesso!")

    except mysql.connector.Error as erro:
        print(f"\n Erro no MySQL: {erro}")

    finally:
        # 4. Encerra a conexão e o cursor
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("\nConexão encerrada.")

if __name__ == "__main__":
    resolver_e_inserir()