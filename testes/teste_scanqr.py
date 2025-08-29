from gerenciador_db import get_pessoa_por_id
from scanners.qr_cam_scanner import ler_qr_camera
from scanners.qr_scanner import ler_qr_imagem



mode = input("Deseja ler QR de imagem(i) ou câmera(c)?")

if mode.lower() == 'i':
    caminho = input("Digite o caminho da imagem QR Code:")
    qr_id = ler_qr_imagem(caminho)
elif mode.lower() =="c":
    qr_id =ler_qr_camera()
else:
    print("Opção invalida")
    ar_id = None

if qr_id:
    pessoa = get_pessoa_por_id(qr_id)
    if pessoa:
        print("Dados da pessoa:",pessoa)
    else:
        print("Pessoa não encontrada no banco")
else:
    print("Nenhum QR code lido")
    
    