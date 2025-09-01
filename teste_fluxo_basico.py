import os
from scanners.qr_generator import gerar_qr_usuario
from scanners.qr_scanner import ler_qr_imagem
from scanners.qr_cam_scanner import ler_qr_camera
from security.fernet_key import carregar_chave
from datetime import datetime

# Função auxiliar para formatar data
def formatar_data(dob_str):
    partes = dob_str.strip().split("/")
    if len(partes) != 3:
        raise ValueError("Formato inválido. Use DD/MM/AAAA")
    dia, mes, ano = partes
    return f"{ano.zfill(4)}-{mes.zfill(2)}-{dia.zfill(2)}"

def teste_fluxo():
    print("\n--- Teste de fluxo completo ---\n")

    # Cadastro de pessoa
    print("Cadastro de nova pessoa:")
    nome = input("Nome: ").strip()
    dob = input("Data de nascimento (DD/MM/AAAA): ").strip()
    cpf = input("ID do documento (CPF): ").strip()
    dob_formatada = formatar_data(dob)

    # Gerar id_curto aleatório
    import random, string
    id_curto = "".join(random.choices(string.hexdigits.lower(), k=8))

    data_usuario = {
        "id_curto": id_curto,
        "nome": nome,
        "cpf": cpf
    }

    # Gerar QR cifrado
    key = carregar_chave()   # bytes
    from cryptography.fernet import Fernet
    cipher = Fernet(key)      # objeto Fernet

    pasta_qr = "qrcodes"
    os.makedirs(pasta_qr, exist_ok=True)
    qr_path = os.path.join(pasta_qr, f"{id_curto}.png")
    gerar_qr_usuario(data_usuario, cipher, qr_path)

    print("\n✅ Pessoa cadastrada com sucesso!")
    print(f"ID curto: {id_curto}")
    print(f"QR Code cifrado gerado em: {qr_path}")

    # Teste leitura QR Code
    escolha = input("\nLer QR Code do usuário (1=imagem, 2=câmera): ").strip()
    if escolha == "1":
        caminho = input("Digite o caminho da imagem do QR Code: ").strip()
        dados_qr = ler_qr_imagem(caminho)
    elif escolha == "2":
        dados_qr = ler_qr_camera()
    else:
        print("Opção inválida.")
        return

    if dados_qr:
        print("\n✅ QR lido com sucesso! Conteúdo:")
        print(dados_qr)
    else:
        print("\n❌ QR não encontrado ou inválido.")

if __name__ == "__main__":
    teste_fluxo()
