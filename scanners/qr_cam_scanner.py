import cv2
import json
from pyzbar.pyzbar import decode
from security.fernet_key import get_cipher

# Carrega o cipher Fernet centralizado
cipher = get_cipher()

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