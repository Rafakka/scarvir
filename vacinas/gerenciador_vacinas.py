from base64 import decode
from datetime import datetime
import os
from tkinter import Image
import psycopg2
import json
from cryptography.fernet import Fernet
from security.fernet_key import get_cipher
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")


def conectar_bd():
    """Cria conexão com o banco."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        return conn
    except Exception as e:
        print("Erro ao conectar no banco:", e)
        return None

def _dict_vacina(row):
    if not row:
        return None
    return {
        "id": row[0],
        "doses_necessarias": row[1],
        "lote": row[2],
        "nome": row[3],
        "fabricante": row[4],
        "validade": row[5],
        "vacinador": row[6]
    }

def get_vacina_por_qr(conteudo_qr):
    if not conteudo_qr:
        return None
    if isinstance(conteudo_qr, bytes):
        try:
            cipher = get_cipher()
            conteudo_qr = cipher.decrypt(conteudo_qr).decode("uft-8")
        except Exception as e:
            print("Erro ao descriptografar QR de vacina", e)
            return None
        if isinstance(conteudo_qr,str):
            try:
                conteudo_qr = json.loads(conteudo_qr)
            except Exception as e:
                print("Erro ao decodificar QR JSON", e)
                return None
        if conteudo_qr.get("kind") != "vaccine":
            print("QR code não é vacina")
            return None
        
        payload = conteudo_qr.get("payload,{}")
        vacina_id = payload.get("id")
        if not vacina_id:
            print("Id da vacina não encontrado no QR")
            return None
    return get_vacina_por_id(vacina_id)

def get_vacina_por_id(vacina_id):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, doses_necessarias, lote, nome, fabricante, validade, vacinador
            FROM vacinas
            WHERE id = %s
        """, (vacina_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return _dict_vacina(row)
    except Exception as e:
        print("Erro ao buscar vacina por ID:", e)
        return None

def get_vacina_por_nome(nome):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, doses_necessarias, lote, nome, fabricante, validade, vacinador
            FROM vacinas
            WHERE nome ILIKE %s
            LIMIT 1
        """, (nome,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return _dict_vacina(row)
    except Exception as e:
        print("Erro ao buscar vacina por nome:", e)
        return None
    
def registrar_dose(pessoa_id, vacina_id, nome_vacinador, data_aplicacao=None):
    if data_aplicacao is None:
        data_aplicacao = datetime.now()

    conn = conectar_bd()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO doses_aplicadas (id_pessoa, id_vacina, numero_doses, data_de_aplicacao, qr_code, vacinador)
            VALUES (%s, %s, 1, %s, NULL, %s)
        """, (pessoa_id, vacina_id, data_aplicacao, nome_vacinador))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Erro ao registrar dose:", e)
        return False
