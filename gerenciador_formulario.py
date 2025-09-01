import os
from datetime import datetime
from scanners.qr_generator import gerar_qr_usuario
from scanners.fernet_key import carregar_chave

# Configurações QR
PASTA_QR = "qrcodes"

# -----------------------------
# Função utilitária: garante pasta
# -----------------------------
def garantir_pasta(caminho):
    if not os.path.exists(caminho):
        os.makedirs(caminho)

# -----------------------------
# Função utilitária: formata data DD/MM/AAAA -> YYYY-MM-DD
# -----------------------------
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

# -----------------------------
# Função principal: cadastro
# -----------------------------
def cadastrar_pessoa():
    # Input com validação de data
    while True:
        nome = input("Nome: ").strip()
        dob = input("Data de nascimento (DD/MM/AAAA): ").strip()
        cpf = input("ID do documento (CPF): ").strip()
        dob_formatada = formatar_data(dob)
        if dob_formatada:
            break
        print("❌ Formato inválido, tente novamente.")

    # Gera id_curto aleatório (baseado no banco) ou pode ser feito aqui, mas deixamos banco gerar
    # Prepare dados do usuário para gerar QR
    data_dict = {
        "nome": nome,
        "cpf": cpf,
        # id_curto será retornado do banco, mas aqui temporário
        "id_curto": None
    }

    try:
        import psycopg2

        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="link217",
            host="localhost"
        )
        cur = conn.cursor()

        # Inserção no banco com id_curto gerado pelo banco
        cur.execute("""
            INSERT INTO pessoas (nome, dob, id_documento, data_de_criacao, id_curto)
            VALUES (%s, %s, %s, NOW(), substring(md5(gen_random_uuid()::text) FROM 1 FOR 8))
            RETURNING id_curto;
        """, (nome, dob_formatada, cpf))

        id_curto = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        data_dict["id_curto"] = id_curto

        # Garantir pasta QR
        garantir_pasta(PASTA_QR)

        # Gera QR cifrado e salva
        qr_path = os.path.join(PASTA_QR, f"{id_curto}.png")
        gerar_qr_usuario(data_dict, qr_path)

        print("\n✅ Pessoa cadastrada com sucesso!")
        print(f"ID curto: {id_curto}")
        print(f"QR Code gerado em: {qr_path}")

        return data_dict, qr_path

    except Exception as e:
        print("Erro no cadastro:", e)
        return None, None

# -----------------------------
# Teste rápido do formulário
# -----------------------------
if __name__ == "__main__":
    cadastrar_pessoa()
