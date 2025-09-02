import os
import json
import qrcode

def _garantir_pasta(path: str):
    pasta = os.path.dirname(path) if os.path.splitext(path)[1] else path
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)

def gerar_qr_cifrado(payload_dict: dict, cipher, path_saida: str) -> str:
    """
    Cifra payload_dict (JSON) e grava QR em path_saida.
    """
    _garantir_pasta(path_saida)
    json_bytes = json.dumps(payload_dict, ensure_ascii=False).encode("utf-8")
    encrypted = cipher.encrypt(json_bytes)
    qr = qrcode.QRCode()
    qr.add_data(encrypted)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(path_saida)
    return path_saida

def gerar_qr_usuario(usuario_dict: dict, cipher, path_saida: str) -> str:
    """
    Envolve o payload com metadados de tipo ('kind') e versão de chave ('kver' futura).
    Mantém compat com seu consumo atual: dados do usuário vão em 'p'.
    """
    payload = {
        "kind": "user",
        "kver": 1,  # reservado p/ rotação futura
        "p": usuario_dict
    }
    return gerar_qr_cifrado(payload, cipher, path_saida)

def gerar_qr_vacina(vacina_dict: dict, cipher, path_saida: str) -> str:
    payload = {
        "kind": "vaccine",
        "kver": 1,
        "p": vacina_dict
    }
    return gerar_qr_cifrado(payload, cipher, path_saida)
