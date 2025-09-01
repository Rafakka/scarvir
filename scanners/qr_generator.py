import qrcode
import json
from cryptography.fernet import Fernet
from scanners.fernet_key import get_cipher

def gerar_qr_usuario(data_dict, path_saida):
    cipher = get_cipher()
    json_bytes = json.dumps(data_dict).encode("utf-8")
    encrypted = cipher.encrypt(json_bytes)

    qr = qrcode.QRCode()
    qr.add_data(encrypted)
    qr.make(fit=True)
    qr_img = qr.make_image()
    qr_img.save(path_saida)
    return path_saida