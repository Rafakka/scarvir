import os
from scanners.qr_scanner import ler_qr_imagem  # futuramente pode chamar ler_qr_camera
from scanners.qr_generator import gerar_qr_usuario, carregar_chave
from gerenciador_db import get_pessoa_por_id_curto, get_pessoa_por_cpf
from gerenciador_formulario import cadastrar_pessoa

def validar_usuario():
    """Tenta validar usuário via QR (imagem ou câmera) e faz fallback por CPF."""
    
    metodo = input("Ler QR Code do usuário (1=imagem, 2=câmera): ").strip()
    
    if metodo == "1":
        caminho = input("Digite o caminho do QR Code: ").strip()
        if not caminho.endswith(".png"):
            caminho += ".png"
        dados_qr = ler_qr_imagem(caminho)
    else:
        # futuramente ler QR da câmera
        dados_qr = None

    pessoa = None
    # 1️⃣ Tenta encontrar pessoa pelo QR
    if dados_qr:
        id_curto = dados_qr.get("id_curto")
        pessoa = get_pessoa_por_id_curto(id_curto)

    # 2️⃣ Se QR falhou ou pessoa não encontrada → fallback CPF
    if not pessoa:
        print("❌ QR inválido ou usuário não encontrado.")
        cpf = input("Digite o CPF do usuário: ").strip()
        pessoa = get_pessoa_por_cpf(cpf)

        if pessoa:
            print("\n✅ Usuário encontrado pelo CPF!")
            # atualiza ou gera QR cifrado
            pasta_qr = "qrcodes"
            os.makedirs(pasta_qr, exist_ok=True)
            cipher = carregar_chave()
            data_usuario = {"id_curto": pessoa[5], "nome": pessoa[1], "cpf": pessoa[3]}
            qr_path = os.path.join(pasta_qr, f"{pessoa[5]}.png")
            gerar_qr_usuario(data_usuario, cipher, qr_path)
            print(f"QR atualizado em: {qr_path}")
        else:
            print("❌ Usuário não encontrado.")
            escolha = input("Deseja cadastrar o usuário? (S/N): ").strip().lower()
            if escolha == "s":
                qr_path, id_curto = cadastrar_pessoa()
                pessoa = get_pessoa_por_id_curto(id_curto)
            else:
                print("Encerrando sistema...")
                return None

    # 3️⃣ Mostra informações básicas do usuário
    if pessoa:
        print("\nDados do usuário:")
        print(f"Nome: {pessoa[1]}")
        print(f"DOB: {pessoa[2]}")
        print(f"CPF: {pessoa[3]}")
        print(f"ID curto: {pessoa[5]}")

    return pessoa
