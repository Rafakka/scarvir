import os
from security.fernet_key import get_cipher
from scanners.qr_generator import gerar_qr_usuario  # Reaproveita função já escrita
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Configurações do DB (já configuradas no seu .env)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

def cadastrar_vacina():
    nome = input("Nome da vacina: ").strip()
    fabricante = input("Fabricante: ").strip()
    lote = input("Lote: ").strip()
    validade = input("Validade (AAAA-MM-DD): ").strip()
    vacinador = input("Vacinador: ").strip()
    doses_necessarias = int(input("Número de doses necessárias: "))

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
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

        # Criar QR da vacina
        cipher = get_cipher()
        data_vacina = {
            "id": vac_id,
            "nome": nome,
            "fabricante": fabricante,
            "lote": lote,
            "validade": validade,
            "vacinador": vacinador,
            "doses_necessarias": doses_necessarias
        }

        pasta_qr = "qrcodes_vacinas"
        os.makedirs(pasta_qr, exist_ok=True)
        qr_path = os.path.join(pasta_qr, f"{vac_id}.png")
        gerar_qr_usuario(data_vacina, cipher, qr_path)

        print(f"\n✅ Vacina cadastrada com sucesso! QR Code salvo em {qr_path}")

        return vac_id, qr_path

    except Exception as e:
        print("Erro ao cadastrar vacina:", e)
        return None, None

if __name__ == "__main__":
    cadastrar_vacina()
