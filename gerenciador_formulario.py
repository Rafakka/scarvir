import os
from scanners.qr_generator import gerar_qr_usuario
from utils.conector_bd import conectar_bd
from validator import validar_cpf, limpar_cpf, validar_e_normalizar_dob, formatar_cpf
from security.fernet_key import get_cipher

def formatar_data(dob_str):
    partes = dob_str.strip().split("/")
    if len(partes) != 3:
        raise ValueError("Formato inválido. Use DD/MM/AAAA")
    dia, mes, ano = partes
    return f"{ano.zfill(4)}-{mes.zfill(2)}-{dia.zfill(2)}"

def perguntar_consentimento() -> bool:
    while True:
        r = input("Você autoriza o uso dos seus dados para cadastro e integração com sistemas externos? (s/n): ").strip().lower()
        if r in ("s", "n"):
            return r == "s"
        print("Resposta inválida. Digite 's' para sim ou 'n' para não.")

def cadastrar_pessoa(conn):
    try:
        # ----- Entrada de dados -----
        nome = input("Nome: ").strip()
        dob_str = input("Data de nascimento (DD/MM/AAAA): ").strip()
        cpf_in = input("ID do documento (CPF): ").strip()

        # ----- Consentimento -----
        consentimento = perguntar_consentimento()
        if not consentimento:
            print("❌ Cadastro cancelado: consentimento necessário.")
            return None, None

        dob_formatada = validar_e_normalizar_dob(dob_str)  # YYYY-MM-DD

    except Exception as e:
        print(f"❌ Erro na data de nascimento: {e}")
        return None, None

    if not validar_cpf(cpf_in):
        print("❌ CPF inválido.")
        return None, None
    
    cpf = limpar_cpf(cpf_in)

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO pessoas (nome, dob, id_documento, data_de_criacao, id_curto, consentimento, consentimento_data)
            VALUES (%s, %s, %s, NOW(), substring(md5(gen_random_uuid()::text) FROM 1 FOR 8), %s, NOW())
            RETURNING id_curto;
        """, (nome, dob_formatada, cpf, True))
        id_curto = cur.fetchone()[0]
        conn.commit()
        cur.close()

    except Exception as e:
        print("Erro ao salvar no banco:", e)
        return None, None
    
    # 4) Gera QR cifrado (somente com consentimento)
    try:
        os.makedirs("qrcodes", exist_ok=True)
        cipher = get_cipher()
        data_usuario = {"id_curto": id_curto, "nome": nome, "cpf": cpf}
        qr_path = os.path.join("qrcodes", f"{id_curto}.png")
        gerar_qr_usuario(data_usuario, cipher, qr_path)
        print("\n✅ Pessoa cadastrada com sucesso!")
        print(f"ID curto: {id_curto}")
        print(f"CPF: {formatar_cpf(cpf)}")
        print(f"QR Code cifrado: {qr_path}")
        usuario_dict = {
            "id": None,
            "nome": nome,
            "dob": dob_formatada,
            "id_documento": cpf,
            "data_de_criacao": None,
            "id_curto": id_curto
        }
        return usuario_dict, qr_path
    except Exception as e:
        print("Erro ao gerar QR:", e)
        return None, None