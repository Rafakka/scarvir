from security.fernet_key import get_cipher
from pyzbar.pyzbar import decode
from PIL import Image
import json

# Carrega o cipher Fernet uma vez
cipher = get_cipher()

def ler_qr_imagem(caminho_imagem):
    """
    Lê QR Code de uma imagem, decifra com Fernet e retorna dict com os dados.
    """
    try:
        img = Image.open(caminho_imagem)
        result = decode(img)
        if not result:
            print("Nenhum QR Code detectado na imagem")
            return None

        encrypted_bytes = result[0].data
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        return json.loads(decrypted_bytes)

    except Exception as e:
        print("Erro ao ler QR da imagem:", e)
        return None
