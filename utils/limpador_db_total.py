import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

def limpar_tabela_pessoas():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cur = conn.cursor()
        cur.execute("DELETE FROM scanlog")
        cur.execute("DELETE FROM doses_aplicadas;")
        cur.execute("DELETE FROM pessoas;")
        cur.execute("DELETE FROM vacinas;")
        cur.execute("TRUNCATE TABLE doses_aplicadas RESTART IDENTITY CASCADE;")
        cur.execute("TRUNCATE TABLE scanlog RESTART IDENTITY CASCADE;")
        cur.execute("TRUNCATE TABLE pessoas RESTART IDENTITY CASCADE;")
        cur.execute("TRUNCATE TABLE vacinas RESTART IDENTITY CASCADE;")
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Tabelas limpas e resetadas com sucesso!")
    except Exception as e:
        print("Erro ao limpar e resetar tabelas:", e)

if __name__ == "__main__":
    limpar_tabela_pessoas()
