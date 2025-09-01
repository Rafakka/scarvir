
import os
import psycopg2
from datetime import datetime
from security.fernet_key import get_cipher
from scanners.qr_generator import gerar_qr_usuario
from dotenv import load_dotenv

load_dotenv()

# Configurações do DB
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

def aplicar_vacina(id_pessoa, id_vacina, numero_doses, qr_code_path):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO doses_aplicadas (id_pessoa, id_vacina, numero_doses, data_de_aplicacao, qr_code)
            VALUES (%s, %s, %s, NOW(), %s)
            RETURNING id;
        """, (id_pessoa, id_vacina, numero_doses, qr_code_path))
        dose_id = cur.fetchone()[0]
        conn.commit()

        print(f"✅ Dose aplicada registrada com ID {dose_id}")

        # Consultar dados completos da pessoa + vacina aplicada
        cur.execute("""
            SELECT p.id, p.nome, p.id_documento, d.id_vacina, v.nome, v.lote, v.fabricante, v.validade, v.vacinador, d.numero_doses, d.data_de_aplicacao
            FROM doses_aplicadas d
            JOIN pessoas p ON d.id_pessoa = p.id
            JOIN vacinas v ON d.id_vacina = v.id
            WHERE d.id = %s;
        """, (dose_id,))
        resultado = cur.fetchone()

        print("\n📋 Dados da pessoa e vacina aplicada:")
        labels = ["Pessoa ID", "Nome", "CPF", "Vacina ID", "Vacina Nome", "Lote", "Fabricante", "Validade", "Vacinador", "Número de doses", "Data de aplicação"]
        for label, valor in zip(labels, resultado):
            print(f"{label}: {valor}")

        cur.close()
        conn.close()

        return resultado

    except Exception as e:
        print("Erro ao aplicar vacina:", e)
        return None

if __name__ == "__main__":
    # Exemplo de IDs (substitua pelos reais do seu DB)
    id_pessoa = int(input("ID da pessoa: "))
    id_vacina = int(input("ID da vacina: "))
    numero_doses = int(input("Número de doses aplicadas: "))

    # QR Code do usuário (fallback)
    qr_code_path = input("Caminho do QR Code do usuário: ")

    aplicar_vacina(id_pessoa, id_vacina, numero_doses, qr_code_path)
