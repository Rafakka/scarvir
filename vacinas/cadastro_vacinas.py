import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

def conectar_bd():
    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
    except Exception as e:
        print("Erro ao conectar no BD:", e)
        return None

def cadastrar_vacina():
    nome = input("Nome da vacina: ").strip()
    fabricante = input("Fabricante: ").strip()
    validade = input("Validade (AAAA-MM-DD): ").strip()
    lote = input("Lote: ").strip()
    vacinador = input("Vacinador: ").strip()

    conn = conectar_bd()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO vacinas (nome, fabricante, validade, lote, vacinador)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (nome, fabricante, validade, lote, vacinador))
        conn.commit()
        id_vacina = cur.fetchone()[0]
        cur.close()
        conn.close()
        print(f"✅ Vacina '{nome}' cadastrada com sucesso! ID: {id_vacina}")
        return id_vacina
    except Exception as e:
        print("Erro ao cadastrar vacina:", e)
        return None
