# gerar_chave.py
from cryptography.fernet import Fernet

# Gera chave secreta
key = Fernet.generate_key()

# Salva em arquivo seguro
with open("secret.key", "wb") as f:
    f.write(key)

print("Chave Fernet gerada e salva em secret.key")