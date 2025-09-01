import os
import psycopg2
from datetime import datetime
from scanners.qr_generator import gerar_qr_usuario
from security.fernet_key import carregar_chave
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

def formatar_data(dob_str):
    partes = dob_str.strip().split("/")
    if len(partes) != 3:
        raise ValueError("Formato inválido. Use DD/MM/AAAA")
    dia, mes, ano = partes
    return f"{ano.zfill(4)}-{mes.zfill(2)}-{dia.zfill(2)}"

def perguntar_consentimento():
    while True:
        resposta = input("Você autoriza o uso dos seus dados para cadastro e integração com sistemas externos? (s/n): ").strip().lower()
        if resposta in ("s", "n"):
            return resposta == "s"
        print("Resposta inválida, digite 's' para sim ou 'n' para não.")

def cadastrar_pessoa():
    try:
        # ----- Entrada de dados -----
        nome = input("Nome: ").strip()
        dob = input("Data de nascimento (DD/MM/AAAA): ").strip()
        cpf = input("ID do documento (CPF): ").strip()
        dob_formatada = formatar_data(dob)

        # ----- Consentimento -----
        consentimento = perguntar_consentimento()
        if not consentimento:
            print("❌ Cadastro cancelado: consentimento necessário.")
            return None, None

        # ----- Conexão e inserção no banco -----
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO pessoas (nome, dob, id_documento, data_de_criacao, id_curto, consentimento, consentimento_data)
            VALUES (%s, %s, %s, NOW(), substring(md5(gen_random_uuid()::text) FROM 1 FOR 8), %s, NOW())
            RETURNING id_curto;
        """, (nome, dob_formatada, cpf, consentimento))
        id_curto = cur.fetchone()[0]
        conn.commit()

        # ----- Geração de QR cifrado -----
        pasta_qr = "qrcodes"
        os.makedirs(pasta_qr, exist_ok=True)

        key = carregar_chave()
        cipher = Fernet(key)
        data_usuario = {"id_curto": id_curto, "nome": nome, "cpf": cpf}
        qr_path = os.path.join(pasta_qr, f"{id_curto}.png")
        gerar_qr_usuario(data_usuario, cipher, qr_path)

        usuario_dict = {
            "id": None,  # Pode buscar se quiser usar RETURNING
            "nome": nome,
            "dob": dob_formatada,
            "id_documento": cpf,
            "data_de_criacao": None,
            "id_curto": id_curto,
            "consentimento": consentimento
        }

        print("\n✅ Pessoa cadastrada com sucesso!")
        print(f"ID curto: {id_curto}")
        print(f"QR Code cifrado gerado em: {qr_path}")

        cur.close()
        conn.close()

        return usuario_dict, qr_path

    except Exception as e:
        print("❌ Erro no cadastro:", e)
        return None, None
