
# coding: iso-8859-1
import connexion
import six


from swagger_server.models.suiv_prod_requete_sql import SuivProdRequeteSql  # noqa: E501
from swagger_server.models.general_liste_valeur import GeneralListeValeur  # noqa: E501
from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.suivi_prod_code import SuiviProdCode  # noqa: E501
from swagger_server.models.suivi_prod_code_list import SuiviProdCodeList  # noqa: E501
from swagger_server.models.suivi_prod_etape_ut import SuiviProdEtapeUt  # noqa: E501
from swagger_server.models.suivi_prod_featuretype import SuiviProdFeaturetype  # noqa: E501
from swagger_server.models.suivi_prod_lot_no_rel import SuiviProdLotNoRel  # noqa: E501
from swagger_server.models.suivi_prod_planification import SuiviProdPlanification  # noqa: E501
from swagger_server.models.suivi_prod_unite_travail2_no_rel import SuiviProdUniteTravail2NoRel  # noqa: E501
from swagger_server import util

#Ajouté manuellement
from flask import request, make_response
from swagger_server.config import db
from swagger_server.controllers import utils_gapi
from swagger_server.controllers import utils_security
from swagger_server.controllers import utils_postgis
from swagger_server.db_models.suivi_prod_db_schema import *
import uuid
from flask import jsonify
#import json

from swagger_server.config import db_view_session
from sqlalchemy.sql import text


def delete_suivi_prod_etape_ut_id(identifiant):  # noqa: E501
    """delete_suivi_prod_etape_ut_id

    Delete a record in etape_ut table. # noqa: E501

    :param identifiant: 
    :type identifiant: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'


def delete_suivi_prod_featuretype_id(identifiant):  # noqa: E501
    """delete_suivi_prod_featuretype_id

    Delete one record from feature_type table. # noqa: E501

    :param identifiant: ID from lot table
    :type identifiant: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'


def delete_suivi_prod_lot_id(identifiant):  # noqa: E501
    """delete_suivi_prod_lot_id

    Delete a record in Lot table. # noqa: E501

    :param identifiant: 
    :type identifiant: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'


def delete_suivi_prod_unite_travail_id(identifiant):  # noqa: E501
    """delete_suivi_prod_unite_travail_id

    Delete a record in table unite_travail_2. # noqa: E501

    :param identifiant: Work area id
    :type identifiant: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'


def get_suivi_prod_code_list(id=None, nom=None):  # noqa: E501
    """get_suivi_prod_code_list

    Obtient un enregistrement de la table suivi_prod.list_codes. # noqa: E501

    :param id: 
    :type id: int
    :param nom: 
    :type nom: str

    :rtype: List[SuiviProdCodeList]
    """
    return 'do some magic!'


def get_suivi_prod_codes(categorie=None, nom=None, id=None, id_list_codes=None):  # noqa: E501
    """get_suivi_prod_codes

    Obtient un enregistrement de la table suivi_prod.code. # noqa: E501

    :param categorie: 
    :type categorie: str
    :param nom: 
    :type nom: str
    :param id: 
    :type id: int
    :param id_list_codes: 
    :type id_list_codes: int

    :rtype: List[SuiviProdCode]
    """
    return 'do some magic!'


def get_suivi_prod_codes_code(code):  # noqa: E501
    """get_suivi_prod_codes_code

     # noqa: E501

    :param code: 
    :type code: str

    :rtype: SuiviProdCode
    """
    # Requête dans la table de Code
    try:
        res = Code.query.filter(Code.id == code).one()
        MASerializer = CodeSchema()
        code_json = MASerializer.dump(res)
    
    except NoResultFound as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    except MultipleResultsFound as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    return jsonify(code_json), 200


def get_suivi_prod_etape_ut_id(identifiant):  # noqa: E501
    """Your GET endpoint

    Retrieve a record from etape_ut table. # noqa: E501

    :param identifiant: 
    :type identifiant: str

    :rtype: SuiviProdEtapeUt
    """
    return 'do some magic!'


def get_suivi_prod_featuretype_id(identifiant):  # noqa: E501
    """Your GET endpoint

    Retreive a record from feature)type table. # noqa: E501

    :param identifiant: ID from lot table
    :type identifiant: str

    :rtype: List[SuiviProdFeaturetype]
    """
    return 'do some magic!'

def get_suivi_prod_requete_bd(body=None, output_format=None, simplifier=None):  # noqa: E501
    """get_suivi_prod_requete_bd

    Permet de lancer une requete SQL au suivi de production et recevoir un JSON ou GeoJSON. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param output_format: 
    :type output_format: str

    :rtype: object
    """
    try:
        # Lecture du body JSON qui contient la requête SQL
        if connexion.request.is_json:
            body = SuivProdRequeteSql.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            raise ValueError("Le service attend un JSON valide contenant la requête")
        
        # Choix du template pour la requête JSON ou GeoJSON?
        if output_format == "json":
            sql_template = """SELECT jsonb_build_object( 
                'RecordCollection', jsonb_agg(feature) 
                ) 
                FROM ( {} 
                ) feature"""
            
            sql_template = sql_template.format(body.sql)

        elif output_format == "geojson":
            #TODO: Vérifier que l'attribut shape est présent. Ou bien chercher dans la requête l'attribut spatial
            geom_attr_name = "shape"

            sql_template = """SELECT jsonb_build_object( 
                'type',     'FeatureCollection', 
                'features', jsonb_agg(feature) 
                ) 
                FROM ( 
                SELECT jsonb_build_object( 
                    'type',       'Feature', 
                    'geometry',   ST_AsGeoJSON(ST_Reverse({}),{},{})::json, 
                    'properties', to_jsonb(inputs) - '{}' 
                ) AS feature 
                FROM (  {} 
                ) inputs 
                ) features"""
            
            if simplifier:
                simplify_string = "ST_Simplify({}, {}, True)".format(geom_attr_name, os.environ.get("GAPI_GEOJSON_TOL_FILTRAGE"))
            else:
                simplify_string = geom_attr_name

            sql_template = sql_template.format(simplify_string, os.environ.get("GAPI_GEOJSON_MAX_DECIMAL"), os.environ.get("GAPI_GEOJSON_PGIS_OPTION"), geom_attr_name, body.sql )
        else:
            raise ValueError("Format de sortie inconnue: {}".format(output_format))
        
        # Lancement de la requête de l'usager vers la BD
        row = db_view_session.execute(text(sql_template)).fetchone()    
        
        return jsonify(row[0]), 200

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 500))            


def get_suivi_prod_lot_id(identifiant, full_relation=None):  # noqa: E501
    """get_suivi_prod_lot_id

    Retrieve a record from Lot table. By using the parameter full_relation&#x3D;False you can retreive only the Lot record or by using full_relation&#x3D;True you can retreive the Lot and all its dependencies (related table records). # noqa: E501

    :param identifiant: 
    :type identifiant: str
    :param full_relation: 
    :type full_relation: str

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def get_suivi_prod_unite_travail_id(identifiant, full_relation=None):  # noqa: E501
    """get_suivi_prod_unite_travail_id

    Retourne un enregistrement de la table suivi-prod.unite_travail_2. En utilisant le paramètre full_relation&#x3D;False vous obtener uniquement l&#x27;enregistrement de la table suivi-prod.unite_travail_2. En utilisant le paramètre full_relation&#x3D;True vous obtenez l&#x27;enregistrement de la table suivi-prod.unite_travail_2 ainsi que toutes ses dépendances (l&#x27;information provenant des tables en relation). # noqa: E501

    :param identifiant: Work area id
    :type identifiant: str
    :param full_relation: 
    :type full_relation: bool

    :rtype: InlineResponse200
    """
    return 'do some magic!'


def get_suivi_prod_unite_travail_listeid_theme_actif(theme):  # noqa: E501
    """Your GET endpoint

    Retourne une liste de ID des unités de travail active selon un thème. # noqa: E501

    :param theme: 
    :type theme: str

    :rtype: GeneralListeValeur
    """
    """
    try:
        pass
        UniteTravail2 = UniteTravail2.query.filter(UniteTravail2.nom_usager == usager).one()
    except expression as identifier:
        pass
    """

    return 'do some magic!'


def post_suivi_prod_etape_ut(body=None):  # noqa: E501
    """post_suivi_prod_etape_ut

    Insert a new record in etape_ut table. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: GeneralMessage
    """
    
    try:
        body = SuiviProdEtapeUt.from_dict(body)  # noqa: E501
        
        token_dict = utils_security.auth_header_to_dict(request.headers.get('Authorization'))
        date_auj = utils_gapi.date_now()

        e_ut = EtapeUt( etampe = "GAPI_"+token_dict["nom_usager"],
                        dt_c = date_auj,
                        dt_m = date_auj,
                        id = str(uuid.uuid4()),
                        id_unite_travail = body.id_ut,
                        nom_etape_cl = body.nom_etape_cl,
                        description = body.description,
                        operateur = body.operateur,
                        date_debut = date_auj,
                        statut_etape_cl = 10101
                        )

        db.session.add(e_ut)
        db.session.flush()

        # Serializer le contenu de l'objet BD en JSON pour le retourner
        MASerializer = EtapeUtSchema()
        e_ut_json = MASerializer.dump(e_ut) 

    except BaseException as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    return jsonify(e_ut_json), 200


def post_suivi_prod_featuretype(body=None):  # noqa: E501
    """post_suivi_prod_featuretype

    Insert feature class inside feature_type table. # noqa: E501

    :param body: 
    :type body: list | bytes

    :rtype: GeneralMessage
    """

    try:
        body = [SuiviProdFeaturetype.from_dict(d) for d in body]
        
        token_dict = utils_security.auth_header_to_dict(request.headers.get('Authorization'))
        date_auj = utils_gapi.date_now()
        out_mess = []

        for v in body:
            ftype = FeatureType(etampe = "GAPI_"+token_dict["nom_usager"],
                                dt_c = date_auj,
                                dt_m = date_auj,
                                id = v.id_lot,
                                local_name = v.local_name,
                                spatial_repres_type_pna = v.spatial_repres_type_pna
                                )    
            db.session.add(ftype)
            out_mess.append(ftype.as_dict())
        
        db.session.flush()
            
    except BaseException as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    return jsonify(out_mess), 200
    

def post_suivi_prod_lot(body=None):  # noqa: E501
    """post_suivi_prod_lot

    Insert a record in Lot table. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: GeneralMessage
    """
    #if connexion.request.is_json:
    
    try:
        #body = SuiviProdLotNoRel.from_dict(connexion.request.get_json())  # noqa: E501
        body = SuiviProdLotNoRel.from_dict(body)
        
        token_dict = utils_security.auth_header_to_dict(request.headers.get('Authorization'))
        date_auj = utils_gapi.date_now()
        
        lot = Lot(  etampe = "GAPI_"+token_dict["nom_usager"],
                    dt_c = date_auj,
                    dt_m = date_auj,
                    id = body.id_lot,
                    operateur = body.operateur,
                    date_debut = body.date_debut,
                    date_fin = body.date_fin,
                    theme_cl = body.theme_cl,
                    type_travail_cl = body.type_travail_cl,
                    statut_lot_cl = body.statut_lot_cl
                    )
        
        db.session.add(lot)
        db.session.flush()

    except BaseException as e:        
        raise Exception(utils_gapi.message_erreur(e, 400))

    return jsonify(lot.as_dict()), 200


def post_suivi_prod_planification(body=None):  # noqa: E501
    """post_suivi_prod_planification

    Service intégrateur permettant la création, selon un thème, d&#x27;un lot et d&#x27;une unité de travail en un seul appel. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: GeneralMessage
    """
    
    body = SuiviProdPlanification.from_dict(body)  # noqa: E501
    
    token_dict = utils_security.auth_header_to_dict(request.headers.get('Authorization'))
    date_auj = utils_gapi.date_now()
    ident_lot = body.id_ut + "_LOT"
    out_mess = []
    
    ### Création du lot
    lot = SuiviProdLotNoRel(id_lot = ident_lot,
                            operateur = token_dict["nom_usager"],
                            date_debut = date_auj,
                            theme_cl = body.theme,
                            type_travail_cl = body.type_travail,
                            statut_lot_cl = 10001
                            )

    ret = post_suivi_prod_lot(eval(str(lot)))
    out_mess.append({"lot":ret[0].get_json()})

    ### Création de la liste de classe
    liste_ft = []
    for classe in body.liste_classes:
        ft = SuiviProdFeaturetype(  id_lot = ident_lot,
                                    local_name = classe,
                                    spatial_repres_type_pna = 635
                                    )
        liste_ft.append(eval(str(ft)))
        
    ret = post_suivi_prod_featuretype(liste_ft)
    out_mess.append({"feature_type":ret[0].get_json()})

    ### Création de l'unite de travail
    ut = SuiviProdUniteTravail2NoRel(   id_ut = body.id_ut,
                                        id_lot = ident_lot,
                                        date_prevue_fin = body.date_fin_prevue,                            
                                        date_debut = date_auj,                                            
                                        where_clause = body.where_clause,
                                        geom = body.geom
                                        )
    
    ret = post_suivi_prod_unite_travail(eval(str(ut)))
    out_mess.append({"unite_travail_2":ret[0].get_json()})
    
    ### Création de l'étape
    e_ut = SuiviProdEtapeUt(id_ut = body.id_ut,
                            nom_etape_cl = 11304,
                            description = "PlanifierZT",
                            operateur = token_dict["nom_usager"],
                            date_debut = date_auj,
                            statut_etape_cl = 10101
                            )
            
    ret = post_suivi_prod_etape_ut(eval(str(e_ut)))
    out_mess.append({"etape_ut":ret[0].get_json()})

    return jsonify(out_mess), 200


def post_suivi_prod_unite_travail(body=None):  # noqa: E501
    """post_suivi_prod_unite_travail

    Insert a new record in unite_travail_2 # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: GeneralMessage
    """
    
    try:
        body = SuiviProdUniteTravail2NoRel.from_dict(body)  # noqa: E501

        token_dict = utils_security.auth_header_to_dict(request.headers.get('Authorization'))
        
        # Validation et reprojection de la géométrie
        body.geom = utils_postgis.validate_geometry(body.geom)

        #conversion de la géométrie en EWKT
        wkt = utils_postgis.convert_geojson_to_wkt(utils_postgis.validate_geometry(body.geom))
        wkt = "SRID={};{}".format(os.environ.get("GAPI_EPSG"), wkt)

        date_auj = utils_gapi.date_now()

        ut = UniteTravail2( etampe = "GAPI_"+token_dict["nom_usager"],
                            dt_c = date_auj,
                            dt_m = date_auj,                            
                            id = body.id_ut,
                            id_lot = body.id_lot,
                            date_prevue_fin = body.date_prevue_fin,                            
                            date_debut = body.date_debut,
                            date_fin = body.date_fin,
                            where_clause = body.where_clause,
                            shape = wkt
                            )

        db.session.add(ut)
        db.session.flush()

    except BaseException as e:        
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    #return GeneralMessage(message=str(ut.as_dict())), 200 
    return jsonify(ut.as_dict()), 200


def put_suivi_prod_etape_ut_id(identifiant, body=None):  # noqa: E501
    """put_suivi_prod_etape_ut_id

    Update a record in etape_ut table. # noqa: E501

    :param identifiant: 
    :type identifiant: str
    :param body: Only not null attributes in the JSON body will get updated. The id must not be empty.
    :type body: dict | bytes

    :rtype: GeneralMessage
    """
    
    try:
        token_dict = utils_security.auth_header_to_dict(request.headers.get('Authorization'))
        date_auj = utils_gapi.date_now()

        rs = EtapeUt.query.filter(EtapeUt.id == identifiant).one()
        
        # Modifier la valeur des champs permis de la table etape_ut selon le contenu du payload
        for k in body.keys():
            if k in ["date_fin", "statut_etape_cl"]:
                setattr(rs, k, body[k])

        # Modifier les champs etampe et dt_m
        rs.etampe = "GAPI_"+token_dict["nom_usager"]
        rs.dt_m = date_auj

        #db.session.commit()

        # Serializer le contenu de l'objet BD en JSON pour le retourner
        MASerializer = EtapeUtSchema()
        e_ut = MASerializer.dump(rs)        

    except BaseException as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    #return GeneralMessage(message=str(e_ut)), 200 
    return jsonify(e_ut), 200


def put_suivi_prod_lot_id(identifiant, body=None):  # noqa: E501
    """put_suivi_prod_lot_id

    Update a record in Lot table. # noqa: E501

    :param identifiant: 
    :type identifiant: str
    :param body: Only not null attributes in the JSON body will get updated. The id must not be empty.
    :type body: dict | bytes

    :rtype: GeneralMessage
    """

    try:
        token_dict = utils_security.auth_header_to_dict(request.headers.get('Authorization'))
        date_auj = utils_gapi.date_now()

        rs = Lot.query.filter(Lot.id == identifiant).one()
        
        # Modifier la valeur des champs permis de la table etape_ut selon le contenu du payload
        for k in body.keys():
            if k in ["date_fin", "statut_lot_cl", "operateur" ]:
                setattr(rs, k, body[k])

        # Modifier les champs etampe et dt_m
        rs.etampe = "GAPI_"+token_dict["nom_usager"]
        rs.dt_m = date_auj

        #db.session.commit()

    except BaseException as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    #return GeneralMessage(message=str(e_ut)), 200 
    return jsonify(rs.as_dict()), 200


def put_suivi_prod_unite_travail_id(identifiant, body=None):  # noqa: E501
    """put_suivi_prod_unite_travail_id

    Update a record in unite_travail_2 table. # noqa: E501

    :param identifiant: Work area id
    :type identifiant: str
    :param body: Seulement les attributs non-null seront mise à jour. Le ID doit toujours avoir une valeur car c&#x27;est la clef de recherche.
    :type body: dict | bytes

    :rtype: GeneralMessage
    """
    try:
        token_dict = utils_security.auth_header_to_dict(request.headers.get('Authorization'))
        date_auj = utils_gapi.date_now()

        rs = UniteTravail2.query.filter(UniteTravail2.id == identifiant).one()
        
        # Modifier la valeur des champs permis de la table etape_ut selon le contenu du payload
        for k in body.keys():
            if k in ["date_fin", "date_prevue_fin" ]:
                setattr(rs, k, body[k])

        # Modifier les champs etampe et dt_m
        rs.etampe = "GAPI_"+token_dict["nom_usager"]
        rs.dt_m = date_auj

        #db.session.commit()

    except BaseException as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    #return GeneralMessage(message=str(e_ut)), 200 
    return jsonify(rs.as_dict()), 200


def get_suivi_prod_type_travail_theme(theme):  # noqa: E501
    """Your GET endpoint

    Retourne une liste des travaux disponibles pour un thème donné. # noqa: E501

    :param theme: 
    :type theme: str

    :rtype: List[SuiviProdCode]
    """
    return 'do some magic!'