import qrcode
import json
from cryptography.fernet import Fernet

def carregar_chave(caminho="secret.key"):
    """Carrega chave Fernet"""
    with open(caminho, "rb") as f:
        key = f.read()
    return Fernet(key)

def gerar_qr_usuario(data_dict, cipher, path_saida):
    """
    Gera QR Code cifrado de um usuário
    """
    # Converte dict para bytes JSON
    json_bytes = json.dumps(data_dict).encode("utf-8")
    # Cifra os bytes
    encrypted = cipher.encrypt(json_bytes)
    # Gera QR
    qr = qrcode.QRCode()
    qr.add_data(encrypted)
    qr.make(fit=True)
    qr_img = qr.make_image()
    qr_img.save(path_saida)
    return path_saida
