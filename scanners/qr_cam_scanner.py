# scanners/qr_scanner.py
from pyzbar.pyzbar import decode
from PIL import Image
import cv2

# --------------------------------------
# Lê QR usando a câmera
# --------------------------------------
def ler_qr_camera(camera_index=0):
    try:
        cap = cv2.VideoCapture(camera_index)
        print("Aponte o QR Code para a câmera... (Pressione 'q' para sair)")
        qr_data = None
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8")
                print("QR Code detectado:", qr_data)
                break

            cv2.imshow("QR Scanner", frame)
            if qr_data or cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return qr_data

    except Exception as e:
        print("Erro ao ler QR da câmera:", e)
        return None
