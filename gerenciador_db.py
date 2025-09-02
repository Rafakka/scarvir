# gerenciador_db.py
import os
import psycopg2
import json
from scanners.qr_scanner import ler_qr_imagem
from scanners.qr_cam_scanner import ler_qr_camera
from dotenv import load_dotenv

# -----------------------------
# Carregar variáveis do .env
# -----------------------------
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

# -----------------------------
# Conexão centralizada com o banco
# -----------------------------
def conectar_bd():
    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
    except Exception as e:
        print("Erro ao conectar ao banco:", e)
        return None


def _dict_pessoa(row):
    if not row:
        return None
    return {
        "id": row[0],
        "nome": row[1],
        "dob": row[2],
        "id_documento": row[3],
        "data_de_criacao": row[4],
        "id_curto": row[5],
        "consentimento": row[6],
        "consentimento_data": row[7]
    }

# -----------------------------
# Funções de busca no banco
# -----------------------------

def get_pessoa_por_id_curto(id_curto):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, dob, id_documento, data_de_criacao, id_curto, consentimento, consentimento_data
            FROM pessoas
            WHERE id_curto = %s
        """, (id_curto,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return _dict_pessoa(row)
    except Exception as e:
        print("Erro ao buscar pessoa pelo ID curto:", e)
        return None

def get_pessoa_por_cpf(cpf):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, dob, id_documento, data_de_criacao, id_curto, consentimento, consentimento_data
            FROM pessoas
            WHERE id_documento = %s
        """, (cpf,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return _dict_pessoa(row)
    except Exception as e:
        print("Erro ao buscar pessoa pelo CPF:", e)
        return None


# -----------------------------
# Função genérica para decodificar QR
# -----------------------------
def get_pessoa_por_qr(conteudo_qr):
    if not conteudo_qr:
        return None

    # Se for string (JSON decodificado do QR cifrado), converte para dict
    if isinstance(conteudo_qr, str):
        try:
            conteudo_qr = json.loads(conteudo_qr)
        except Exception as e:
            print("Erro ao decodificar QR JSON:", e)
            return None

    id_curto = conteudo_qr.get("id_curto")
    if not id_curto:
        print("ID curto não encontrado no QR Code")
        return None

    # Busca a pessoa pelo ID curto (já retorna dict)
    pessoa = get_pessoa_por_id_curto(id_curto)
    if not pessoa:
        print("Pessoa não encontrada no banco para este ID curto")
        return None

    return pessoa

# -----------------------------
# Funções específicas de leitura
# -----------------------------
def get_pessoa_por_qr_imagem(caminho_imagem):
    conteudo_qr = ler_qr_imagem(caminho_imagem)
    if not conteudo_qr:
        print("Nenhum QR Code detectado na imagem")
        return None
    return get_pessoa_por_qr(conteudo_qr)

def get_pessoa_por_qr_camera():
    conteudo_qr = ler_qr_camera()
    if not conteudo_qr:
        print("Nenhum QR Code detectado na câmera")
        return None
    return get_pessoa_por_qr(conteudo_qr)

