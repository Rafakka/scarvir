import psycopg2
import json
from scanners.qr_scanner import ler_qr_imagem, ler_qr_camera

# Configurações do banco
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "link217"
DB_HOST = "localhost"

# -----------------------------
# Busca pessoa pelo id_curto no banco
# -----------------------------
def get_pessoa_por_id_curto(id_curto):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT id, id_curto, nome, dob, id_documento, data_de_criacao
            FROM pessoas
            WHERE id_curto = %s
        """, (id_curto,))
        pessoa = cur.fetchone()
        cur.close()
        conn.close()
        return pessoa
    except Exception as e:
        print("Erro ao buscar pessoa:", e)
        return None

# -----------------------------
# Busca pessoa a partir de um QR Code (imagem)
# -----------------------------
def get_pessoa_por_qr_imagem(caminho_imagem):
    conteudo_qr = ler_qr_imagem(caminho_imagem)
    if not conteudo_qr:
        print("Nenhum QR Code detectado na imagem")
        return None

    try:
        dados = json.loads(conteudo_qr)
        id_curto = dados.get("id_curto")
        if not id_curto:
            print("ID curto não encontrado no QR Code")
            return None
        return get_pessoa_por_id_curto(id_curto)
    except Exception as e:
        print("Erro ao decodificar QR Code:", e)
        return None

# -----------------------------
# Busca pessoa a partir de um QR Code (câmera)
# -----------------------------
def get_pessoa_por_qr_camera():
    conteudo_qr = ler_qr_camera()
    if not conteudo_qr:
        print("Nenhum QR Code detectado na câmera")
        return None

    try:
        dados = json.loads(conteudo_qr)
        id_curto = dados.get("id_curto")
        if not id_curto:
            print("ID curto não encontrado no QR Code")
            return None
        return get_pessoa_por_id_curto(id_curto)
    except Exception as e:
        print("Erro ao decodificar QR Code da câmera:", e)
        return None

# -----------------------------
# Exemplo de teste rápido
# -----------------------------
if __name__ == "__main__":
    # Testar leitura de imagem
    caminho_teste = input("Digite o caminho da imagem do QR Code: ").strip()
    pessoa_imagem = get_pessoa_por_qr_imagem(caminho_teste)
    if pessoa_imagem:
        print("✅ Pessoa encontrada na imagem:", pessoa_imagem)
    else:
        print("❌ Pessoa não encontrada na imagem")

    # Testar leitura pela câmera
    usar_camera = input("Deseja testar leitura pela câmera? (s/n): ").strip().lower()
    if usar_camera == "s":
        pessoa_camera = get_pessoa_por_qr_camera()
        if pessoa_camera:
            print("✅ Pessoa encontrada na câmera:", pessoa_camera)
        else:
            print("❌ Pessoa não encontrada na câmera")
