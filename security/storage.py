import json
from security import fernet

def save_data(filename, data):
    """Salva os dados criptografados em JSON."""
    encrypted_data = fernet.encrypt(json.dumps(data).encode())
    with open(filename, "wb") as f:
        f.write(encrypted_data)

def load_data(filename):
    """Carrega os dados descriptografados do JSON."""
    with open(filename, "rb") as f:
        encrypted_data = f.read()
    return json.loads(fernet.decrypt(encrypted_data).decode())