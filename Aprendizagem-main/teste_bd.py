import os
import mysql.connector
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

def criar_tabelas():
    try:
        # Estabelece a conexão com o MySQL
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "G&Ncode@2026"),
            database=os.getenv("DB_NAME", "planilha_db"),
            port=int(os.getenv("DB_PORT", 3306))
        )

        cursor = conexao.cursor()

        # Tabela 1: Usuários
        sql_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Tabela 2: Lançamentos / Registros da Planilha
        sql_lancamentos = """
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NOT NULL,
            descricao VARCHAR(255) NOT NULL,
            valor DECIMAL(10, 2) NOT NULL,
            tipo ENUM('RECEITA', 'DESPESA') NOT NULL,
            data_lancamento DATE NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        );
        """

        # Executa os comandos SQL
        print("Criando tabela 'usuarios'...")
        cursor.execute(sql_usuarios)

        print("Criando tabela 'lancamentos'...")
        cursor.execute(sql_lancamentos)

        # Confirma as alterações
        conexao.commit()
        print("\n Tabelas criadas com sucesso no banco 'planilha_db'!")

    except mysql.connector.Error as erro:
        print(f"\n Erro ao criar tabelas: {erro}")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

if __name__ == "__main__":
    criar_tabelas()