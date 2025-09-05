from datetime import date
import os
import json
import qrcode
from gerenciador_vacinas import get_vacina_por_id
from security.fernet_key import get_cipher
from gerenciador_db import conectar_bd

def gerar_qr_vacina(vacina_id):
    conn = conectar_bd()
    if not conn:
        return None, None
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, fabricante, lote, validade, vacinador, doses_necessarias
            FROM vacinas 
            WHERE id = %s
        """, (vacina_id,))
        vacina = cur.fetchone()
        cur.close()
        conn.close()

        if not vacina:
            print("Vacina não encontrada")
            return None, None
        validade = vacina[4]
        if isinstance(validade, date):
            validade = validade.isoformat()  # Converte para string "YYYY-MM-DD"
        
        vacina_dict = {
            "id": vacina[0],
            "nome": vacina[1],
            "fabricante": vacina[2],
            "lote": vacina[3],
            "validade": validade,  # Agora é string
            "vacinador": vacina[5],
            "doses_necessarias": vacina[6]
        }


        qr_dict = {
            "kind":"vaccine",
            "payload":vacina_dict
        }

        cipher = get_cipher()
        json_bytes = json.dumps(qr_dict).encode("utf-8")
        encrypted = cipher.encrypt(json_bytes)

        pasta_qr="qrcodes_vacinas"
        os.makedirs(pasta_qr, exist_ok=True)
        path_saida = os.path.join(pasta_qr,f"{vacina_dict['id']}.png")

        qr = qrcode.QRCode()
        qr.add_data(encrypted)
        qr.make(fit=True)
        qr_img = qr.make_image()
        qr_img.save(path_saida)

        print(f"Qrcode de vacina gerado:{path_saida}")
        return vacina_dict,path_saida
    
    except Exception as e:
        print("Erro ao gerar QR da vacina:", e)
        return None, None
    
def ler_qr_camera_vacina():
        """Lê QR code da câmera para vacina (adaptado)"""
        from pyzbar.pyzbar import decode
        import cv2
        from security.fernet_key import get_decrypt_ciphers
        import json

        cap = cv2.VideoCapture(0)
        print("Aproxime o QR Code da vacina da câmera. Pressione 'q' para cancelar.")

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    continue

                decoded_objs = decode(frame)
                if decoded_objs:
                    encrypted_bytes = decoded_objs[0].data
                    return encrypted_bytes  # Retorna bytes cifrados

                cv2.imshow("Leitura de QR Vacina", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
        
        return None

def ler_qr_imagem_vacina(caminho_imagem):
    """Lê QR code de imagem para vacina (adaptado)"""
    from pyzbar.pyzbar import decode
    from PIL import Image
    import json

    try:
        img = Image.open(caminho_imagem)
        result = decode(img)
        if result:
            return result[0].data  # Retorna bytes cifrados
        return None
    except Exception as e:
        print(f"Erro ao ler imagem: {e}")
        return None
    
def get_vacina_por_qr(conteudo_qr):
    if not conteudo_qr:
        return None
    
    # Se for bytes (diretamente do QR)
    if isinstance(conteudo_qr, bytes):
        try:
            from security.fernet_key import get_decrypt_ciphers
            for cipher in get_decrypt_ciphers():
                try:
                    decrypted = cipher.decrypt(conteudo_qr)
                    conteudo_qr = json.loads(decrypted.decode('utf-8'))
                    break
                except:
                    continue
        except Exception as e:
            print("Erro ao descriptografar QR:", e)
            return None
    
    # Verificar se é vacina
    if not isinstance(conteudo_qr, dict) or conteudo_qr.get("kind") != "vaccine":
        print("QR code não é de vacina")
        return None
    
    payload = conteudo_qr.get("payload", {})
    vacina_id = payload.get("id")
    
    if not vacina_id:
        print("ID da vacina não encontrado no QR")
        return None
    
    return get_vacina_por_id(vacina_id)