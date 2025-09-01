import cv2
from pyzbar.pyzbar import decode
from cryptography.fernet import Fernet
import json
import os

# Carrega chave Fernet
KEY_PATH = os.path.join(os.path.dirname(__file__), "secret.key")
with open(KEY_PATH, "rb") as f:
    key = f.read()
cipher = Fernet(key)

def ler_qr_camera():
    """
    Abre câmera, lê QR Code, decifra com Fernet e retorna dict com os dados.
    Pressione 'q' para sair da câmera.
    """
    cap = cv2.VideoCapture(0)
    print("Aproxime o QR Code da câmera. Pressione 'q' para cancelar.")

    pessoa_dados = None
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        decoded_objs = decode(frame)
        if decoded_objs:
            dados_cifrados = decoded_objs[0].data
            try:
                json_bytes = cipher.decrypt(dados_cifrados)
                pessoa_dados = json.loads(json_bytes)
                print("QR Code lido com sucesso!")
            except Exception as e:
                print("Erro ao decodificar QR Code da câmera:", e)
            break

        cv2.imshow("Leitura de QR", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return pessoa_dados
