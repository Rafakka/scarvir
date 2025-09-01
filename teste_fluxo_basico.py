from gerenciador_formulario import cadastrar_pessoa
from gerenciador_db import (
    get_pessoa_por_qr_imagem,
    get_pessoa_por_qr_camera,
    get_pessoa_por_cpf
)
from scanners.qr_generator import gerar_qr_usuario
from security.fernet_key import get_cipher

def teste_fluxo():
    print("\n--- Teste de fluxo completo ---\n")

    # 1️⃣ Cadastro de nova pessoa
    print("Cadastro de nova pessoa:")
    usuario = cadastrar_pessoa()  # retorna tuple ou dict conforme sua função
    cipher = get_cipher()
    
    # Gera QR cifrado
    qr_path = gerar_qr_usuario(usuario, cipher)
    print(f"\nQR Code gerado em: {qr_path}")

    # 2️⃣ Leitura de QR Code
    try:
        escolha = input("Ler QR Code do usuário (1=imagem, 2=câmera): ").strip()
        if escolha == "1":
            caminho = input("Digite o caminho da imagem do QR Code: ").strip()
            pessoa = get_pessoa_por_qr_imagem(caminho)
        elif escolha == "2":
            pessoa = get_pessoa_por_qr_camera()
        else:
            pessoa = None
    except Exception as e:
        print("Erro ao ler QR Code:", e)
        pessoa = None

    # 3️⃣ Fallback por CPF se QR inválido
    if not pessoa:
        print("\nQR não encontrado ou inválido. Fallback por CPF.")
        cpf = input("Digite o CPF da pessoa: ").strip()
        pessoa = get_pessoa_por_cpf(cpf)

    # 4️⃣ Exibe dados
    if pessoa:
        if isinstance(pessoa, tuple):
            # tupla do DB -> dict para exibição
            pessoa_dict = {
                "id": pessoa[0],
                "nome": pessoa[1],
                "dob": pessoa[2],
                "cpf": pessoa[3],
                "data_de_criacao": pessoa[4],
                "id_curto": pessoa[5],
            }
        else:
            pessoa_dict = pessoa

        print("\n✅ Usuário encontrado com sucesso!")
        for k, v in pessoa_dict.items():
            print(f"{k}: {v}")
    else:
        print("\n❌ Usuário não encontrado!")

if __name__ == "__main__":
    teste_fluxo()
