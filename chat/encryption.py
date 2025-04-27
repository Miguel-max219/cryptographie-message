import base64
import re
from cryptography.fernet import Fernet

key = b'ZsD2kQ9gH5oDQOaPfUkl7ZMN9Yb7zyDQnQHbHdvj61Q='
cipher_suite = Fernet(key)

def decrypt(token):
    try:
        if is_base64(token):
            return cipher_suite.decrypt(token.encode()).decode()
        else:
            return "[Texte non chiffré]"
    except Exception as e:
        return f"[Erreur de déchiffrement: {e}]"

def is_base64(s):
    return bool(re.fullmatch(r'^[A-Za-z0-9+/]+={0,2}$', s))
