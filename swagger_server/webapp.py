#!/usr/bin/env python3

from swagger_server import encoder

from swagger_server import config

from swagger_server.config import app
from swagger_server.config import db
from swagger_server.config import db_view_session

from swagger_server.utils import utils_security

from flask import Response, request, g
from flask import jsonify
import re

from flask_admin.contrib import sqla
from swagger_server.db_models.api_db_schema import *


connex_app = config.connex_app
connex_app.add_api('swagger.yaml', arguments={'title': 'geosys-api'}, pythonic_params=True)
connex_app.app.json_encoder = encoder.JSONEncoder

@app.before_request
def before_request_func():
    # Peuple la variable globale de session g.user_lang avec la valeur transmise par
    # l'usager dans l'entête de sa requête. "fr" est la valeur par défaut quand on ne 
    # peut pas la déterminer à partir de la requête du client
    lang = request.headers.get("Accept-Language")
    if lang is None:
        g.user_lang = "fr"
    elif re.search("fr", lang, re.IGNORECASE) is not None:
        g.user_lang = "fr"
    elif re.search("en|us|gb|ang", lang, re.IGNORECASE) is not None:
        g.user_lang = "en"
    else:
        g.user_lang = "fr"


# Toute erreur de type Exception soulevée dans le code aboutira ici
@app.errorhandler(Exception)
def your_exception_handler(exception):    
    
    db.session.rollback()
    
    if isinstance(exception.args[0], Response):
        return exception.args[0]
    else:
        return jsonify(message=str(exception)), 500

# Ce code est toujours exécuté à la fin de chaque session avec un usager de l'API
@app.teardown_request
def teardown_request_func(error=None):    
    db.session.commit()
    db.session.remove()
    db_view_session.remove()
   

#if __name__ == '__main__':
#    connex_app.run(port=8080)


# ************************
# Section pour Flask-Admin
# ************************

# Création des onglets de gestion pour les tables usager_geosys et cle_aws
class UsagerGeosysView(sqla.ModelView):
    column_display_pk = True
    column_list = ['usager_id', 'nom_usager', 'mot_de_passe', 'themes', 'scopes', 'equipes', 'cle_aws',]
    form_columns = ['nom_usager', 'mot_de_passe', 'themes', 'scopes', 'equipes', 'cle_aws',]

class CleAwView(sqla.ModelView):
    column_display_pk = True
    column_list = ['id', 'acces_id', 'acces_secret', 'desc',]
    form_columns = ['id', 'acces_id', 'acces_secret', 'desc',]
    
# Add views
config.admin.add_view(UsagerGeosysView(UsagerGeosys, db.session))
config.admin.add_view(CleAwView(CleAw, db.session))

# L'usager entre un mot de passe en clair et celui-ci est encrypté après le insert ou le update.
# On ne conserve que le mot de passe encrypté dans la table des usagers
@db.event.listens_for(UsagerGeosys, "after_insert")
@db.event.listens_for(UsagerGeosys, "after_update")
def encrypt_user_password(mapper, connection, target):
    tbl_usager = UsagerGeosys.__table__
    pwd = utils_security.encrypt_password(target.mot_de_passe)    
    
    connection.execute(tbl_usager.update().where(tbl_usager.c.usager_id==target.usager_id).values(mot_de_passe=pwd))
