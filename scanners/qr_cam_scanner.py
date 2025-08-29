from base64 import decode
import cv2

def ler_qr_camera():
    cap = cv2.VideoCapture(0)
    print("Posicione o QR Code na frente da câmera. Pressione 'q' para sair.")

    conteudo = None
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            conteudo = obj.data.decode("utf-8")
            print("QR detectado:", conteudo)
            cap.release()
            cv2.destroyAllWindows()
            return conteudo

        cv2.imshow("Leitura QR", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return conteudo
