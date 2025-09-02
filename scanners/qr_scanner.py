from security.fernet_key import get_decrypt_ciphers
from pyzbar.pyzbar import decode
from PIL import Image
import json

def _decifra(encrypted: bytes):
    for cipher in get_decrypt_ciphers():
        try:
            plain = cipher.decrypt(encrypted)
            return json.loads(plain)
        except Exception:
            continue
    raise ValueError("Falha ao decifrar com todas as chaves disponíveis.")

def _extrair_payload(d: dict):
    # Aceita tanto formato antigo (chaves “id_curto”, “nome”...) quanto novo {"kind":..., "p": {...}}
    if isinstance(d, dict) and "p" in d and "kind" in d:
        return d["kind"], d["p"]
    return "unknown", d

def ler_qr_imagem(caminho_imagem):
    try:
        img = Image.open(caminho_imagem)
        result = decode(img)
        if not result:
            return None
        encrypted_bytes = result[0].data
        data = _decifra(encrypted_bytes)
        kind, payload = _extrair_payload(data)
        return {"kind": kind, "payload": payload}
    except Exception as e:
        print("Erro ao ler QR da imagem:", e)
        return None