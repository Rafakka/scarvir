# teste_fluxo_vacina.py
import os
import json
from security.fernet_key import get_cipher
from vacinas.gerenciador_vacinas import cadastrar_vacina, gerar_qr_vacina
from pyzbar.pyzbar import decode
from PIL import Image

def ler_qr_imagem(caminho_imagem):
    """Lê e decifra QR Code de vacina"""
    try:
        img = Image.open(caminho_imagem)
        result = decode(img)
        if not result:
            print("Nenhum QR Code detectado na imagem")
            return None
        encrypted_bytes = result[0].data
        cipher = get_cipher()
        decrypted = cipher.decrypt(encrypted_bytes)
        return json.loads(decrypted)
    except Exception as e:
        print("Erro ao ler QR da imagem:", e)
        return None

def teste_fluxo():
    print("\n--- Teste de fluxo completo de Vacina ---\n")

    # 1️⃣ Cadastro manual
    vac_id = cadastrar_vacina()
    if not vac_id:
        print("❌ Cadastro de vacina falhou. Encerrando teste.")
        return

    # 2️⃣ Gerar QR Code cifrado
    qr_path = gerar_qr_vacina(vac_id)
    if not qr_path:
        print("❌ Geração de QR Code falhou. Encerrando teste.")
        return

    # 3️⃣ Ler QR Code
    print("\nTentando ler QR Code da vacina...")
    dados_lidos = ler_qr_imagem(qr_path)
    if not dados_lidos:
        print("❌ Falha ao ler QR Code.")
        return

    print("\n✅ QR Code lido com sucesso. Dados retornados:")
    for k, v in dados_lidos.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    teste_fluxo()
