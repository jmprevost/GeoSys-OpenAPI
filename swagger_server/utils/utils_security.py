from swagger_server.utils import utils_gapi
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken
import jwt

def create_encryption_key(pwd_clair):
    """create_encryption_key:

    Création de la clé d'encryption selon la librairie Fernet.
    Cette clé peut être ensuite utilisée pour encrypter ou décrypter un mot de passe.

    :param pwd_clair: Mot de passe en texte et lisible par un être humain
    :type pwd_clair: str
    
    :rtype: str
    """
    salt = os.environ.get("GAPI_CRYPTO_SALT")
    pwd_clair = pwd_clair.encode()

    # Creation de la cle d'encryption
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=int(os.environ.get("GAPI_CRYPTO_ITERATION")),
        backend=default_backend()
    )    
    key = base64.urlsafe_b64encode(kdf.derive(pwd_clair))

    return Fernet(key)

def encrypt_password(pwd_clair):
    """encrypt_password:

    Encrypte un mot de passe selon l'algorithme de Fernet. Retourne une
    chaine de caractères correspondant au mot de passe encrypté.

    :param pwd_clair: Mot de passe en texte et lisible par un être humain
    :type pwd_clair: str
    
    :rtype: str
    """

    crypto_key = create_encryption_key(pwd_clair)
    pwd_encrypt = crypto_key.encrypt(pwd_clair.encode())
    
    return pwd_encrypt.decode()
    """
    salt = os.environ.get("GAPI_CRYPTO_SALT")
    pwd_clair = pwd_clair.encode()

    # Creation de la cle d'encryption
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=int(os.environ.get("GAPI_CRYPTO_ITERATION")),
        backend=default_backend()
    )    
    key = base64.urlsafe_b64encode(kdf.derive(pwd_clair))

    f = Fernet(key)

    pwd_encrypt = f.encrypt(pwd_clair)
    print("encode: {}".format(pwd_encrypt))
    print("encode: {}".format(pwd_encrypt.decode()))
    return pwd_encrypt.decode()
    """

def password_checker(pwd_clair, pwd_encrypt):
    """password_checker:

    Vérifie si le mot de passe en clair (en texte et lisible par un être humain)
    correspond au mot de passe encrypté provenant la BD des usagers Geosys.
    On décrypte le mot de passe encrypté (pwd_encrypt) et on regarde s'il correspond
    au mot de passe en clair qui a été passé en paramètre.

    :param pwd_clair: Mot de passe en texte et lisible par un être humain
    :type pwd_clair: str
    :param pwd_encrypt: Mot de passe encrypté provenant de la BD
    :type pwd_encrypt: str
    
    :rtype: Boolean
    """

    crypto_key = create_encryption_key(pwd_clair)
    try:
        # Le résultat du .decrypt est en byte
        if crypto_key.decrypt(pwd_encrypt.encode()) == pwd_clair.encode():
            return True
        else:
            return False

    except InvalidToken:
        return False
    
    """
    pwd_to_check = encrypt_password(pwd_clair)
    
    if pwd_to_check == pwd_encrypt:
        return True
    else:
        return False
    """
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
    """    

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
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    return token_content