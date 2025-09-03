from datetime import date
import os
import json
import qrcode
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