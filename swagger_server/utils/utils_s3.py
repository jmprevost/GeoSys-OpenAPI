from swagger_server.utils import utils_security
from swagger_server.utils import utils_gapi

import boto3
import os
from werkzeug.utils import secure_filename
from flask import request
import mimetypes

def check_bucket_trailing_slash(contenant_url):
    """check_bucket_trailing_slash

    Vérifie si le url du contenant S3 se termine par un slash. On en ajoute un s'il n'y en a pas.

    :param contenant_url: url du contenant S3
    :type contenant_url: str
    
    :rtype: str
    """        
    contenant_url = str(contenant_url).strip()
    contenant_url = str(contenant_url).lstrip("/")    
    if str(contenant_url).endswith("/") or len(str(contenant_url)) == 0:
        return contenant_url
    else:
        return contenant_url + "/"

def check_s3_theme_access( themes, s3_path ):
    """check_s3_theme_access

    Compare la liste de thème passée en paramètre avec le url s3. Les url dans s3 pour Geosys on la structure suivante:
    <environnement (de, tst, pro, etc.)>/<travail ou ressources>/themes/<un nom de thème>/...

    Cette fonction vérifie si dans la liste des thèmes fournit en paramètre il y en a un qui correspond à ../<un nom de thème>/... du url donné en paramètre
    
    La liste des thèmes à vérifier provient des thèmes permis pour un usager Geosys. Cette liste se trouve dans son token.

    :param themes: Liste des thèmes à vérifier
    :type themes: List[]
    :param s3_path: url s3 à vérifier
    :type s3_path: str
    
    :rtype: Boolean
    """

    parts = str(s3_path).split("/")
    if len(parts) > 4:
        return set([parts[3]]).issubset(set(themes)) #retour True ou False
    else:
        return True

def check_s3_obj_existance(s3_client, obj_url):
    """check_s3_obj_existance

    Vérifie si le url du contenant S3 se termine par un slash. On en ajoute un s'il n'y en a pas.

    :param s3_client: session d'un client dans S3
    :type s3_client: boto3.Client
    :param obj_url: URL d'un objet conservé dans S3
    :type obj_url: str
    
    :rtype: True ou une Exception
    """
    # Requête vers S3
    result = s3_client.list_objects_v2(Bucket=os.environ.get("GAPI_AWS_S3_BUCKET_NAME"), Prefix=obj_url, Delimiter='/')
    
    #Vérifie si le URL est bon
    if result.get('KeyCount') == 0:
        raise Exception(utils_gapi.message_erreur("Le URL: {} n'existe pas".format(obj_url), 400))
    
    return True
    
def get_s3_session(s3_url):
    """get_s3_session

    Création d'un objet session s3 à partir des clés d'accès contenu dans le token de l'usager.
    Il faut donner le url s3 que l'on veut accéder car il possible que l'usager n'est pas accès
    à celui-ci (voir fonction: check_s3_theme_access). Il faut que l'usager soit autorisé à accéder ce url
    pour que la session s3 soit ouverte.

    :param contenant_url: url s3 à vérifier
    :type contenant_url: str
    
    :rtype: boto3.session.Session
    """
    
    # Lecture du token
    token_dict = utils_security.auth_header_to_dict(request.headers.get('Authorization'))

    # Vérification si l'usager a le droit d'accéder à URL
    if check_s3_theme_access( token_dict["theme_nom"], s3_url ) == False:
        message = "Accès interdit! Vos thèmes permis sont: {}. Le URL que vous voulez accéder est: {}".format(token_dict["theme_nom"], s3_url)
        raise Exception(utils_gapi.message_erreur(message, 400))

    # Connexion à S3
    s3_session = boto3.session.Session(region_name = os.environ.get("GAPI_AWS_REGION"),
                aws_access_key_id = token_dict["aws_access"]["acces_id"],
                aws_secret_access_key = token_dict["aws_access"]["acces_secret"]
    )

    return s3_session

def create_s3_object(contenant_url, contenu=None):
    """create_s3_object

    Création d'un objet s3.
    - Si le paramètre contenu est vide alors la fonction créera un répertoire dans s3
    - Si le paramètre contenu n'est pas vide alors la fonction téléversera le contenu dans s3 et création le chemin s'il n'existe pas.

    :param contenant_url: url s3 à créer
    :type contenant_url: str
    :param contenu: fichier à téléverser
    :type contenu: werkzeug.FileStorage()
    
    :rtype: str
    """

    # Création d'une session s3
    ma_session = get_s3_session(contenant_url)
    client = ma_session.client("s3")
    bucket_name = os.environ.get("GAPI_AWS_S3_BUCKET_NAME")

    # Le paramètre "contenant_url" doit se terminer par un "/"
    if str(contenant_url).endswith("/") == False:            
        contenant_url = contenant_url + "/"

    message = ""
    if contenu == None:
        
        # Création d'un répertoire
        client.put_object(Bucket=bucket_name, Key=contenant_url)
        message = "Le dossier: {} a été créé.".format(contenant_url)
    
    else:
        # Copie du fichier dans S3
        fsize = get_size(contenu)        
        fname = secure_filename(contenu.filename)
        fichier_url = str(contenant_url)+str(fname)

        if contenu.content_type == None or contenu.content_type == "":
            content_type = mimetypes.MimeTypes().guess_type(fname)[0]
        else:
            content_type = contenu.content_type
        
        # Si le fichier à copier dépasse une certaine limite, on le téléverse en plusieurs morceau au lieu d'un seul.
        if fsize < int(os.environ.get("GAPI_AWS_S3_MULTI_PART_CHUNK_SIZE")):            
            client.put_object(Body=contenu, Bucket=bucket_name, Key=fichier_url, ContentType=content_type)
        else:            
            upload_s3_multi_part(client, fichier_url, contenu, bucket_name)
        
        message = "Le fichier: {} a été téléversé.".format(fichier_url)
    
    return message

def get_total_bytes(s3_client, fichier_url):
    """get_total_bytes

    Retourne la taille d'un fichier stocké dans s3    

    :param s3_client: objet client permettant d'interagir avec s3
    :type s3_client: boto3.Client
    :param fichier_url: url du fichier dans s3
    :type fichier_url: str
    
    :rtype: int
    """
    # Check si le URL exist
    result = s3_client.list_objects(Bucket=os.environ.get("GAPI_AWS_S3_BUCKET_NAME"))
    for item in result['Contents']:
        if item['Key'] == fichier_url:
            return item['Size']


def get_s3_object(s3_client, fichier_url):
    """get_s3_object

    Télécharge un fichier à partir de s3

    :param s3_client: objet client permettant d'interagir avec s3
    :type s3_client: boto3.Client
    :param fichier_url: url du fichier dans s3
    :type fichier_url: str
    
    :rtype: StreamingBody()
    """
    
    total_bytes = get_total_bytes(s3_client, fichier_url)
    chunk_size = int(os.environ.get("GAPI_AWS_S3_MULTI_PART_CHUNK_SIZE"))

    # Si le fichier à téélécharger dépasse une certaine limite, on le télécharge en plusieurs morceau au lieu d'un seul.
    if total_bytes > chunk_size:
        return get_s3_object_range(s3_client, fichier_url, total_bytes)

    return s3_client.get_object(Bucket=os.environ.get("GAPI_AWS_S3_BUCKET_NAME"), Key=fichier_url)['Body'].read()


def get_s3_object_range(s3_client, fichier_url, total_bytes):
    """get_s3_object_range

    Sépare le fichier à télécharger en morceau avant de le télécharger.

    :param s3_client: objet client permettant d'interagir avec s3
    :type s3_client: boto3.Client
    :param fichier_url: url du fichier dans s3
    :type fichier_url: str
    :param total_bytes: taille en bytes du fichier à télécharger 
    :type total_bytes: int
    
    :rtype: StreamingBody()
    """

    offset = 0
    chunk_size = int(os.environ.get("GAPI_AWS_S3_MULTI_PART_CHUNK_SIZE"))
    
    while total_bytes > 0:
        end = offset + (chunk_size-1) if total_bytes > chunk_size else ""
        total_bytes -= chunk_size
        
        byte_range = 'bytes={offset}-{end}'.format(offset=offset, end=end)
        offset = end + 1 if not isinstance(end, str) else None
        
        yield s3_client.get_object(Bucket=os.environ.get("GAPI_AWS_S3_BUCKET_NAME"), Key=fichier_url, Range=byte_range)['Body'].read()


def upload_s3_multi_part(s3_client, fichier_url, contenu, bucket_name):
    """upload_s3_multi_part

    Sépare li fichier à téléverser en morceau avant de la téléverser

    :param s3_client: objet client permettant d'interagir avec s3
    :type s3_client: boto3.Client
    :param fichier_url: url du fichier dans s3
    :type fichier_url: str
    :param contenu: fichier à télécharger 
    :type contenu: werkzeug.FileStorage()
    :param bucket_name: nom du contenant où l'on veut téléverser le fichier 
    :type bucket_name: str
    
    :rtype: str
    """

    psize = int(os.environ.get("GAPI_AWS_S3_MULTI_PART_CHUNK_SIZE"))    
    part = 0
    part_info = { 'Parts': [] }
    bucket_name = os.environ.get("GAPI_AWS_S3_BUCKET_NAME")

    disposition = 'attachment; filename="{}"'.format(str(secure_filename(contenu.filename)))
    
    try:
        # Initialisation. Annoncer à s3 que le fichier sera chargé en plusieurs parties
        mp = s3_client.create_multipart_upload(Bucket=bucket_name, 
                                               Key=fichier_url,
                                               ContentType=contenu.content_type,
                                               ContentDisposition=disposition
                                               )
        
        # Boucler pour téléverser chaque partie du fichier
        while True:
            body = contenu.read(psize)
            if body:
                part += 1

                resp = s3_client.upload_part(Bucket=bucket_name,
                                             Body=body,
                                             Key=fichier_url,
                                             PartNumber=part,
                                             UploadId=mp['UploadId']
                                            )
                
                # Conserver l'information de chacune des parties
                part_info['Parts'].append(
                        {
                            'ETag': resp['ETag'],
                            'PartNumber': part
                        }
                    )
            else:
                break
        
        # Annoncer à s3 que toutes les parties ont été téléversées
        s3_client.complete_multipart_upload(Bucket=bucket_name,
                                            Key=fichier_url,
                                            MultipartUpload=part_info,
                                            UploadId=mp['UploadId']
                                            )
        
    except Exception as e:
        if mp:
            s3_client.abort_multipart_upload(Bucket=bucket_name,
                                             Key=fichier_url,
                                             UploadId=mp['UploadId'])
        raise e
            
def get_size(fobj):
    """get_size

    Détermine la taille du fichier à téléverser. Le fichier est en streaming donc il n'existe pas
    sur le disque. Il faut parcourir le stream sans le lire pour connaitre sa taille totale.

    :param fobj: fichier à téléverser 
    :type fobj: werkzeug.FileStorage()
    
    :rtype: int
    """
    # Il arrive parfois que la taille du fichier est déjà spécifiée dans le header
    if fobj.content_length:
        return fobj.content_length

    # Parcourir le fichier pour déterminer sa taille
    try:
        pos = fobj.tell()
        fobj.seek(0, 2)  #seek to end
        size = fobj.tell()
        fobj.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError) as e:
        return e

    # Si le fichier en mémoire ne supporte pas le seek et le tell
    return 0  # On suppose qu'il est petit
