from cryptography.fernet import Fernet
import os

# Caminho único para a chave
KEY_PATH = os.path.join(os.path.dirname(__file__), "secret.key")

def gerar_chave():
    """Gera uma nova chave e salva no arquivo"""
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    return key

def carregar_chave():
    """Carrega a chave existente do arquivo, ou cria se não existir"""
    if not os.path.exists(KEY_PATH):
        return gerar_chave()
    with open(KEY_PATH, "rb") as f:
        key = f.read()
    return key

def get_cipher():
    """Retorna o objeto Fernet já inicializado"""
    key = carregar_chave()
    return Fernet(key)
