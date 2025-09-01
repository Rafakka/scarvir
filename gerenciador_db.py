import psycopg2
import json
from scanners.qr_scanner import ler_qr_imagem
from scanners.qr_cam_scanner import ler_qr_camera

# Configurações do banco
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "link217"
DB_HOST = "localhost"

# -----------------------------
# Funções de busca no banco
# -----------------------------
def get_pessoa_por_id_curto(id_curto):
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, dob, id_documento, data_de_criacao, id_curto
            FROM pessoas
            WHERE id_curto = %s
        """, (id_curto,))
        pessoa = cur.fetchone()
        cur.close()
        conn.close()
        return pessoa
    except Exception as e:
        print("Erro ao buscar pessoa pelo id_curto:", e)
        return None

def get_pessoa_por_cpf(cpf):
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, dob, id_documento, data_de_criacao, id_curto
            FROM pessoas
            WHERE id_documento = %s
        """, (cpf,))
        pessoa = cur.fetchone()
        cur.close()
        conn.close()
        return pessoa
    except Exception as e:
        print("Erro ao buscar pessoa pelo CPF:", e)
        return None

# -----------------------------
# Função genérica para decodificar QR
# -----------------------------
def get_pessoa_por_qr(conteudo_qr):
    if not conteudo_qr:
        return None
    id_curto = conteudo_qr.get("id_curto")
    if not id_curto:
        print("ID curto não encontrado no QR Code")
        return None
    return get_pessoa_por_id_curto(id_curto)

# -----------------------------
# Funções específicas de leitura
# -----------------------------
def get_pessoa_por_qr_imagem(caminho_imagem):
    conteudo_qr = ler_qr_imagem(caminho_imagem)
    if not conteudo_qr:
        print("Nenhum QR Code detectado na imagem")
    return get_pessoa_por_qr(conteudo_qr)

def get_pessoa_por_qr_camera():
    conteudo_qr = ler_qr_camera()
    if not conteudo_qr:
        print("Nenhum QR Code detectado na câmera")
    return get_pessoa_por_qr(conteudo_qr)
