from cryptography.fernet import Fernet
import os

KEY_FILE = "./security/secret.key"

def load_key():
    """Carrega a chave do arquivo ou cria uma nova se não existir."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

# Aqui você carrega e já cria a instância do Fernet
FERNET_KEY = load_key()
fernet = Fernet(FERNET_KEY)