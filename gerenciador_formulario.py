import os
import qrcode
import psycopg2
from datetime import datetime

# Função para garantir que a pasta existe
def garantir_pasta(caminho):
    if not os.path.exists(caminho):
        os.makedirs(caminho)

def cadastrar_pessoa():
    nome = input("Nome: ")
    dob = input("Data de nascimento (YYYY-MM-DD): ")
    id_documento = input("ID do documento: ")

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="link217",
            host="localhost"
        )
        cur = conn.cursor()

        # insere pessoa e retorna id gerado
        cur.execute("""
            INSERT INTO pessoas (nome, dob, id_documento, data_de_criacao)
            VALUES (%s, %s, %s, NOW())
            RETURNING id;
        """, (nome, dob, id_documento))

        pessoa_id = cur.fetchone()[0]
        conn.commit()

        # Garantir que a pasta existe
        pasta_qr = "qrcodes"
        garantir_pasta(pasta_qr)

        # Gerar QR Code
        qr = qrcode.make(str(pessoa_id))
        qr_path = os.path.join(pasta_qr, f"{pessoa_id}.png")
        qr.save(qr_path)

        print(f"Pessoa cadastrada com ID {pessoa_id}. QR Code gerado em {qr_path}")

        cur.close()
        conn.close()

    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    cadastrar_pessoa()
