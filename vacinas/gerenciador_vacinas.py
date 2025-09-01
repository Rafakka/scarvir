import os
import psycopg2
import json
import qrcode
from cryptography.fernet import Fernet
from security.fernet_key import get_cipher
from dotenv import load_dotenv

# Carrega variáveis do .env
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


def cadastrar_vacina():
    """Cadastra uma vacina manualmente no banco."""
    nome = input("Nome da vacina: ").strip()
    fabricante = input("Fabricante: ").strip()
    lote = input("Lote: ").strip()
    validade = input("Validade (AAAA-MM-DD): ").strip()
    vacinador = input("Vacinador responsável: ").strip()
    doses_necessarias = input("Número total de doses necessárias: ").strip()

    conn = conectar_bd()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO vacinas (nome, fabricante, lote, validade, vacinador, doses_necessarias)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (nome, fabricante, lote, validade, vacinador, doses_necessarias))
        vac_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        print(f"\n✅ Vacina cadastrada com sucesso! ID: {vac_id}")
        return vac_id
    except Exception as e:
        print("Erro ao cadastrar vacina:", e)
        return None


def gerar_qr_vacina(vacina_id):
    """Gera QR Code para a vacina usando Fernet."""
    conn = conectar_bd()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, fabricante, lote, validade, vacinador
            FROM vacinas
            WHERE id = %s
        """, (vacina_id,))
        vacina = cur.fetchone()
        cur.close()
        conn.close()

        if not vacina:
            print("Vacina não encontrada.")
            return None

        # Transformar tupla em dict
        vacina_dict = {
            "id": vacina[0],
            "nome": vacina[1],
            "fabricante": vacina[2],
            "lote": vacina[3],
            "validade": vacina[4],
            "vacinador": vacina[5]
        }

        # Gerar QR cifrado
        cipher = get_cipher()
        json_bytes = json.dumps(vacina_dict).encode("utf-8")
        encrypted = cipher.encrypt(json_bytes)

        pasta_qr = "qrcodes_vacinas"
        os.makedirs(pasta_qr, exist_ok=True)
        path_saida = os.path.join(pasta_qr, f"{vacina_dict['id']}.png")

        qr = qrcode.QRCode()
        qr.add_data(encrypted)
        qr.make(fit=True)
        qr_img = qr.make_image()
        qr_img.save(path_saida)

        print(f"✅ QR Code gerado: {path_saida}")
        return path_saida

    except Exception as e:
        print("Erro ao gerar QR da vacina:", e)
        return None
