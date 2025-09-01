from pyzbar.pyzbar import decode
from PIL import Image
from cryptography.fernet import Fernet
import json
import os

KEY_PATH = os.path.join(os.path.dirname(__file__), "secret.key")
with open(KEY_PATH, "rb") as f:
    key = f.read()
cipher = Fernet(key)

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

        dados_cifrados = result[0].data  # bytes cifrados do QR
        json_bytes = cipher.decrypt(dados_cifrados)  # decifra
        dados = json.loads(json_bytes)  # bytes -> dict
        return dados
    except Exception as e:
        print("Erro ao ler QR da imagem:", e)
        return None
