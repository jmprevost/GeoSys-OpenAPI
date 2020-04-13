import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken
import jwt

def password_checker(pwd_clair, pwd_encrypt):
    """password_checker:

    Vérifie si le mot de passe en clair (en texte et lisible par un être humain)
    correspond au mot de passe encrypté provenant la BD des usagers Geosys

    :param pwd_clair: Mot de passe en texte et lisible par un être humain
    :type pwd_clair: str
    :param pwd_encrypt: Mot de passe encrypté provenant de la BD
    :type pwd_encrypt: str
    
    :rtype: Boolean
    """
    pwd_clair = pwd_clair.encode()
    pwd_encrypt = pwd_encrypt.encode()
    salt = os.environ.get("GAPI_CRYPTO_SALT")
    
    # Creation de la cle d'encryption
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=int(os.environ.get("GAPI_CRYPTO_ITERATION")),
        backend=default_backend()
    )    
    key = base64.urlsafe_b64encode(kdf.derive(pwd_clair))
    
    # Decryption du mot de passe encrypte passe en parametre et
    # comparaison avec le mot de passe en clair pass� en parametre         
    f = Fernet(key)
    
    try:
        if f.decrypt(pwd_encrypt) == pwd_clair:
            return True
        else:
            return False

    except InvalidToken:
        return False

def auth_header_to_dict( auth_header ):
    """auth_header_to_dict:

    Cette fonction convertit le token encrypté en dictionnaire python.

    :param auth_header: Token encrypté de l'usager
    :type auth_header: str
    
    :rtype: dict{}
    """
    auth_type, token = auth_header.split(None, 1)

    JWT_SECRET = os.environ.get("GAPI_CRYPTO_SALT")
    JWT_ALGORITHM = os.environ.get("GAPI_JWT_ALGORITHM")
    try:
        token_content = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception as e:
        print (e)
    
    return token_content