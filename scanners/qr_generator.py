import os
import qrcode
import json
from cryptography.fernet import Fernet

def gerar_qr_usuario(data_dict, cipher, path_saida=None):
    """Gera QR cifrado a partir do dict de usuário."""
    json_bytes = json.dumps(data_dict).encode('utf-8')
    encrypted = cipher.encrypt(json_bytes)

    qr = qrcode.QRCode()
    qr.add_data(encrypted)
    qr.make(fit=True)
    qr_img = qr.make_image()

    if not path_saida:
        pasta = "qrcodes"
        os.makedirs(pasta, exist_ok=True)
        path_saida = os.path.join(pasta, f"{data_dict['id_curto']}.png")

    qr_img.save(path_saida)
    return path_saida