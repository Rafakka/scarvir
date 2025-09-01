import os
import qrcode
import json
from cryptography.fernet import Fernet
from security.fernet_key import get_cipher

def gerar_qr_usuario(data_dict, cipher, path_saida=None):
    """Gera QR cifrado a partir do dict de usuário.
    Se path_saida não fornecido, salva em 'qrcodes/{id_curto}.png'
    """
    json_bytes = json.dumps(data_dict).encode('utf-8')
    encrypted = cipher.encrypt(json_bytes)
    cipher = get_cipher()

    qr = qrcode.QRCode()
    qr.add_data(encrypted)
    qr.make(fit=True)
    qr_img = qr.make_image()

    if isinstance(data_dict, tuple):
    # converter a tupla para dict esperado
        data_dict = {
            "id": data_dict[0],
            "nome": data_dict[1],
            "dob": data_dict[2],
            "id_documento": data_dict[3],
            "data_de_criacao": data_dict[4],
            "id_curto": data_dict[5],
        }

    if not path_saida:
        pasta = "qrcodes"
        if not os.path.exists(pasta):
            os.makedirs(pasta)
        path_saida = os.path.join(pasta, f"{data_dict['id_curto']}.png")

    qr_img.save(path_saida)
    return path_saida