from gerenciador_formulario import cadastrar_pessoa
from gerenciador_db import (
    get_pessoa_por_id_curto,
    get_pessoa_por_cpf,
    get_pessoa_por_qr_imagem,
    get_pessoa_por_qr_camera
)

def main():
    print("=== Teste do fluxo completo ===\n")

    # 1️⃣ Cadastrar pessoa e gerar QR
    print("--- Cadastro de pessoa ---")
    cadastrar_pessoa()

    # 2️⃣ Testar leitura de QR via imagem
    print("\n--- Teste de leitura de QR via imagem ---")
    caminho = input("Digite o caminho da imagem do QR Code gerado: ").strip()
    pessoa_qr = get_pessoa_por_qr_imagem(caminho)
    if pessoa_qr:
        print("✅ Pessoa encontrada via QR imagem:", pessoa_qr)
    else:
        print("❌ QR não encontrado ou inválido")

    # 3️⃣ Testar leitura de QR via câmera
    print("\n--- Teste de leitura de QR via câmera ---")
    pessoa_camera = get_pessoa_por_qr_camera()
    if pessoa_camera:
        print("✅ Pessoa encontrada via QR câmera:", pessoa_camera)
    else:
        print("❌ QR não detectado na câmera")

    # 4️⃣ Testar fallback via CPF
    print("\n--- Teste fallback CPF ---")
    cpf = input("Digite o CPF para busca manual: ").strip()
    pessoa_cpf = get_pessoa_por_cpf(cpf)
    if pessoa_cpf:
        print("✅ Pessoa encontrada via CPF:", pessoa_cpf)
    else:
        print("❌ Pessoa não encontrada via CPF")

if __name__ == "__main__":
    main()
