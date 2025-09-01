import os
import qrcode
import psycopg2
from datetime import datetime

# Configurações do banco
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "link217"
DB_HOST = "localhost"

# Função para garantir que a pasta existe
def garantir_pasta(caminho):
    if not os.path.exists(caminho):
        os.makedirs(caminho)

# Formata data de nascimento DD/MM/AAAA -> YYYY-MM-DD (PostgreSQL)
def formatar_data(dob_str):
    dia, mes, ano = dob_str.split("/")
    return f"{ano}-{mes}-{dia}"

# Função principal de cadastro
def cadastrar_pessoa():
    nome = input("Nome: ").strip()
    dob = input("Data de nascimento (DD/MM/AAAA): ").strip()
    cpf = input("ID do documento (CPF): ").strip()

    dob_formatada = formatar_data(dob)

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cur = conn.cursor()

        # Insere pessoa com id_curto gerado pelo banco (função substring(md5(UUID)) do PostgreSQL)
        cur.execute("""
            INSERT INTO pessoas (nome, dob, id_documento, data_de_criacao, id_curto)
            VALUES (%s, %s, %s, NOW(), substring(md5(gen_random_uuid()::text) FROM 1 FOR 8))
            RETURNING id_curto;
        """, (nome, dob_formatada, cpf))

        id_curto = cur.fetchone()[0]
        conn.commit()

        # Gera QR Code
        pasta_qr = "qrcodes"
        garantir_pasta(pasta_qr)

        qr = qrcode.make(id_curto)
        qr_path = os.path.join(pasta_qr, f"{id_curto}.png")
        qr.save(qr_path)

        print(f"\n✅ Pessoa cadastrada com sucesso!")
        print(f"ID curto: {id_curto}")
        print(f"QR Code gerado em: {qr_path}")

        cur.close()
        conn.close()

    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    cadastrar_pessoa()
