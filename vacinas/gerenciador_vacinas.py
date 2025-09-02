from base64 import decode
from datetime import datetime
import os
from tkinter import Image
import cv2
import psycopg2
import json
import qrcode
from cryptography.fernet import Fernet
from security.fernet_key import get_cipher
from dotenv import load_dotenv

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


# Função genérica para decodificar QR cifrado

def get_vacina_por_qr(conteudo_qr):
    if not conteudo_qr:
        return None

    # Se for string (JSON decodificado do QR cifrado), converte para dict
    if isinstance(conteudo_qr, str):
        try:
            conteudo_qr = json.loads(conteudo_qr)
        except Exception as e:
            print("Erro ao decodificar QR JSON:", e)
            return None

    return conteudo_qr  # já é dict com os dados da vacina

# -----------------------------
# Funções específicas de leitura
# -----------------------------

def get_vacina_por_qr_imagem(caminho_imagem):
    """Lê QR Code da imagem e retorna dict da vacina."""
    try:
        img = Image.open(caminho_imagem)
        result = decode(img)
        if not result:
            print("Nenhum QR Code detectado na imagem")
            return None

        encrypted_bytes = result[0].data
        cipher = get_cipher()
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        dados_vacina = json.loads(decrypted_bytes)
        return get_vacina_por_qr(dados_vacina)
    except Exception as e:
        print("Erro ao ler QR da imagem:", e)
        return None

def get_vacina_por_qr_camera():
    """Lê QR Code via câmera e retorna dict da vacina."""
    cap = cv2.VideoCapture(0)
    print("Aproxime o QR Code da vacina da câmera. Pressione 'q' para cancelar.")

    dados_vacina = None
    cipher = get_cipher()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        decoded_objs = decode(frame)
        if decoded_objs:
            encrypted_bytes = decoded_objs[0].data
            try:
                decrypted_bytes = cipher.decrypt(encrypted_bytes)
                dados_vacina = json.loads(decrypted_bytes)
                print("QR Code da vacina lido com sucesso!")
            except Exception as e:
                print("Erro ao decodificar QR Code da vacina:", e)
            break

        cv2.imshow("Leitura de QR Vacina", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return get_vacina_por_qr(dados_vacina)


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
