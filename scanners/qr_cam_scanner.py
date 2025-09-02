import cv2
from pyzbar.pyzbar import decode
import json
from security.fernet_key import get_decrypt_ciphers

def _decifra(encrypted: bytes):
    for cipher in get_decrypt_ciphers():
        try:
            plain = cipher.decrypt(encrypted)
            return json.loads(plain)
        except Exception:
            continue
    raise ValueError("Falha ao decifrar com todas as chaves disponíveis.")

def _extrair_payload(d: dict):
    if isinstance(d, dict) and "p" in d and "kind" in d:
        return d["kind"], d["p"]
    return "unknown", d

def ler_qr_camera():
    cap = cv2.VideoCapture(0)
    print("Aproxime o QR Code da câmera. Pressione 'q' para cancelar.")

    payload_final = None
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            decoded_objs = decode(frame)
            if decoded_objs:
                encrypted_bytes = decoded_objs[0].data
                try:
                    data = _decifra(encrypted_bytes)
                    kind, payload = _extrair_payload(data)
                    payload_final = {"kind": kind, "payload": payload}
                    print("✅ QR Code lido com sucesso!")
                except Exception as e:
                    print("Erro ao decodificar QR da câmera:", e)
                break

            cv2.imshow("Leitura de QR", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return payload_final