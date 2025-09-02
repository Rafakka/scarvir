from cryptography.fernet import Fernet
import os
from glob import glob

# Compat: ainda usamos secret.key por padrão
BASE_DIR = os.path.dirname(__file__)
LEGACY_KEY_PATH = os.path.join(BASE_DIR, "secret.key")

# Preparado para rotação futura: chaves em security/keys/fernet_v*.key
KEYS_DIR = os.path.join(BASE_DIR, "keys")
os.makedirs(KEYS_DIR, exist_ok=True)

def _load_key(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def _ensure_legacy_key() -> bytes:
    if not os.path.exists(LEGACY_KEY_PATH):
        with open(LEGACY_KEY_PATH, "wb") as f:
            f.write(Fernet.generate_key())
    return _load_key(LEGACY_KEY_PATH)

def get_cipher() -> Fernet:
    """Cipher principal (criptografar). Hoje: secret.key. Futuro: última versão em keys/."""
    # Hoje mantemos a legacy por compatibilidade
    key = _ensure_legacy_key()
    return Fernet(key)

def get_decrypt_ciphers():
    """Lista de ciphers para decodificar (suporta rotação: tenta todas)."""
    ciphers = []
    # Legacy primeiro (maior chance de sucesso hoje)
    ciphers.append(get_cipher())
    # Depois, quaisquer chaves adicionais em security/keys/
    for path in sorted(glob(os.path.join(KEYS_DIR, "fernet_v*.key"))):
        try:
            ciphers.append(Fernet(_load_key(path)))
        except Exception:
            pass
    return ciphers
