from scanners.fernet_key import get_cipher
from pyzbar.pyzbar import decode
from PIL import Image
from cryptography.fernet import Fernet
import json
import os

def ler_qr_imagem(caminho_imagem):
    try:
        img = Image.open(caminho_imagem)
        result = decode(img)
        if not result:
            return None
        encrypted_bytes = result[0].data
        cipher = get_cipher()
        decrypted = cipher.decrypt(encrypted_bytes)
        return json.loads(decrypted)
    except Exception as e:
        print("Erro ao ler QR da imagem:", e)
        return None
