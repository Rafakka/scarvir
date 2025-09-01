
from gerenciador_formulario import cadastrar_pessoa
from gerenciador_db import get_pessoa_por_qr_imagem, get_pessoa_por_cpf

def teste_fluxo():
    print("\n--- Teste de fluxo completo com consentimento ---\n")
    
    # 1️⃣ Cadastro da pessoa
    usuario, qr_path = cadastrar_pessoa()
    if not usuario:
        print("❌ Cadastro não realizado. Encerrando teste.")
        return
    
    print(f"\n✅ Usuário cadastrado com QR Code em: {qr_path}")

    # 2️⃣ Leitura do QR (imagem)
    print("\nTentando ler QR Code via imagem...")
    usuario_lido = get_pessoa_por_qr_imagem(qr_path)
    if usuario_lido:
        print("✅ QR Code lido com sucesso. Dados retornados:")
        if isinstance(usuario_lido, dict):
            for k, v in usuario_lido.items():
                print(f"{k}: {v}")
        else:
            print(usuario_lido)
    else:
        print("❌ Falha ao ler QR Code da imagem. Tentando fallback por CPF...")
        usuario_lido = get_pessoa_por_cpf(usuario['id_documento'])
        if usuario_lido:
            print("✅ Usuário encontrado via CPF:")
            print(usuario_lido)
        else:
            print("❌ Usuário não encontrado nem via QR nem CPF. Encerrando teste.")
            return

if __name__ == "__main__":
    teste_fluxo()
