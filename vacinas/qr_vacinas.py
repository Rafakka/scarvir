import os
import qrcode
import json
from cryptography.fernet import Fernet
from security.fernet_key import get_cipher

def gerar_qr_vacina(vacina_dict, path_saida=None):
    cipher = get_cipher()
    json_bytes = json.dumps(vacina_dict).encode('utf-8')
    encrypted = cipher.encrypt(json_bytes)

    qr = qrcode.QRCode()
    qr.add_data(encrypted)
    qr.make(fit=True)
    qr_img = qr.make_image()

    if not path_saida:
        pasta = "qrcodes_vacinas"
        os.makedirs(pasta, exist_ok=True)
        path_saida = os.path.join(pasta, f"{vacina_dict['id']}.png")

    qr_img.save(path_saida)
    print(f"✅ QR da vacina gerado em: {path_saida}")
    return path_saida
