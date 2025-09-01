from gerenciador_formulario import cadastrar_pessoa
from scanners.qr_scanner import ler_qr_imagem

qr_path, _ = cadastrar_pessoa()

caminho = input("\nDigite o caminho do QR Code para leitura: ").strip()
dados = ler_qr_imagem(caminho)
if dados:
    print("\n✅ QR lido com sucesso!")
    print(dados)
else:
    print("❌ QR inválido ou não encontrado")
