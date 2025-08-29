from pyzbar.pyzbar import decode
from PIL import Image

def ler_qr_imagem(caminho_imagem):
    try:
        img = Image.open(caminho_imagem)
        result = decode(img)
        if result:
            return result[0].data.decode("utf-8")
        else:
            return None
    except Exception as e:
        print("Erro ao ler QR:", e)
        return None