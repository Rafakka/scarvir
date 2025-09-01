from pyzbar.pyzbar import decode
from PIL import Image
import json
from cryptography.fernet import Fernet

def carregar_chave(caminho="secret.key"):
    with open(caminho, "rb") as f:
        key = f.read()
    return Fernet(key)

def ler_qr_imagem(caminho_imagem):
    try:
        img = Image.open(caminho_imagem)
        result = decode(img)
        if result:
            qr_data = result[0].data
            cipher = carregar_chave()
            decrypted_bytes = cipher.decrypt(qr_data)
            data = json.loads(decrypted_bytes)
            return data
        else:
            return None
    except Exception as e:
        print("Erro ao decodificar QR Code:", e)
        return None
