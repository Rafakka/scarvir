import os
import psycopg2
from datetime import datetime
from scanners.qr_generator import gerar_qr_usuario, carregar_chave

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "link217"
DB_HOST = "localhost"

def formatar_data(dob_str):
    partes = dob_str.strip().split("/")
    if len(partes) != 3:
        raise ValueError("Formato inválido. Use DD/MM/AAAA")
    dia, mes, ano = partes
    return f"{ano.zfill(4)}-{mes.zfill(2)}-{dia.zfill(2)}"

def cadastrar_pessoa():
    while True:
        try:
            nome = input("Nome: ").strip()
            dob = input("Data de nascimento (DD/MM/AAAA): ").strip()
            cpf = input("ID do documento (CPF): ").strip()
            dob_formatada = formatar_data(dob)
            break
        except Exception as e:
            print("❌ Formato inválido, tente novamente.")

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cur = conn.cursor()

        # Inserir pessoa no banco, gerar id_curto pelo banco
        cur.execute("""
            INSERT INTO pessoas (nome, dob, id_documento, data_de_criacao, id_curto)
            VALUES (%s, %s, %s, NOW(), substring(md5(gen_random_uuid()::text) FROM 1 FOR 8))
            RETURNING id_curto;
        """, (nome, dob_formatada, cpf))
        id_curto = cur.fetchone()[0]
        conn.commit()

        # Criar pasta QR
        pasta_qr = "qrcodes"
        os.makedirs(pasta_qr, exist_ok=True)

        # Gerar QR cifrado
        cipher = carregar_chave()
        data_usuario = {"id_curto": id_curto, "nome": nome, "cpf": cpf}
        qr_path = os.path.join(pasta_qr, f"{id_curto}.png")
        gerar_qr_usuario(data_usuario, cipher, qr_path)

        print("\n✅ Pessoa cadastrada com sucesso!")
        print(f"ID curto: {id_curto}")
        print(f"QR Code cifrado gerado em: {qr_path}")

        cur.close()
        conn.close()

        return qr_path, id_curto

    except Exception as e:
        print("Erro:", e)
        return None, None
