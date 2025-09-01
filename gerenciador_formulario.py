import os
import qrcode
import psycopg2
import json

from gerenciador_db import get_pessoa_por_id

# Configurações do banco
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "link217"
DB_HOST = "localhost"

# Função para garantir que a pasta existe
def garantir_pasta(caminho):
    if not os.path.exists(caminho):
        os.makedirs(caminho)

# Formata e valida a data de nascimento
def formatar_data(dob_str):
    try:
        partes = dob_str.strip().split("/")
        if len(partes) != 3:
            raise ValueError("Formato inválido. Use DD/MM/AAAA")
        dia, mes, ano = partes
        if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
            raise ValueError("Data deve conter apenas números")
        return f"{ano.zfill(4)}-{mes.zfill(2)}-{dia.zfill(2)}"
    except Exception as e:
        print("Erro ao formatar data:", e)
        return None

# Função principal de cadastro
def cadastrar_pessoa():
    # --- Nome ---
    while True:
        nome = input("Nome: ").strip()
        if nome:
            break
        print("❌ Nome não pode ser vazio")

    # --- Data de nascimento ---
    while True:
        dob = input("Data de nascimento (DD/MM/AAAA): ").strip()
        dob_formatada = formatar_data(dob)
        if dob_formatada:
            break
        print("❌ Formato inválido, tente novamente.")

    # --- CPF ---
    while True:
        cpf = input("ID do documento (CPF): ").strip()
        if cpf:
            break
        print("❌ CPF não pode ser vazio")

    # --- Conexão com o banco ---
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cur = conn.cursor()

        # Insere pessoa com id_curto gerado pelo banco
        cur.execute("""
            INSERT INTO pessoas (nome, dob, id_documento, data_de_criacao, id_curto)
            VALUES (%s, %s, %s, NOW(), substring(md5(gen_random_uuid()::text) FROM 1 FOR 8))
            RETURNING id_curto;
        """, (nome, dob_formatada, cpf))

        id_curto = cur.fetchone()[0]
        conn.commit()

        # --- Gera QR Code com JSON ---
        pasta_qr = "qrcodes"
        garantir_pasta(pasta_qr)

        # Cria um dicionário com os dados que queremos no QR
        dados_qr = {
            "id_curto": id_curto,
            "nome": nome,
            "cpf": cpf
        }

        # Converte para string JSON
        qr_json = json.dumps(dados_qr, ensure_ascii=False)

        qr = qrcode.make(qr_json)
        qr_path = os.path.join(pasta_qr, f"{id_curto}.png")
        qr.save(qr_path)

        print(f"\n✅ Pessoa cadastrada com sucesso!")
        print(f"ID curto: {id_curto}")
        print(f"QR Code gerado em: {qr_path}")
        print(f"Conteúdo do QR: {qr_json}")

        cur.close()
        conn.close()

    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    cadastrar_pessoa()
    get_pessoa_por_id()
