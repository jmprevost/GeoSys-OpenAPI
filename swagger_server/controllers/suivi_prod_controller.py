
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
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from flask import request, make_response
from swagger_server.config import db
from swagger_server.utils import utils_gapi
from swagger_server.utils import utils_security
from swagger_server.utils import utils_postgis
from swagger_server.db_models.suivi_prod_db_schema import *
import uuid
from flask import jsonify
from swagger_server.utils import erreurs


from swagger_server.config import db_view_session
from sqlalchemy.sql import text

from flask import Response


def delete_suivi_prod_etape_ut_id(identifiant):  # noqa: E501
    """delete_suivi_prod_etape_ut_id

    Delete a record in etape_ut table. # noqa: E501

    :param identifiant: 
    :type identifiant: str

    :rtype: GeneralMessage
    """

    try:
        etp_ut = EtapeUt.query.filter(EtapeUt.id == identifiant).one()        
        db.session.delete(etp_ut)
        db.session.flush()

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    mess = "L'étape {} a été effacée de la table etape_ut".format(etp_ut.id)
    return jsonify(message=mess), 200


def delete_suivi_prod_featuretype_id(identifiant):  # noqa: E501
    """delete_suivi_prod_featuretype_id

    Delete one record from feature_type table. # noqa: E501

    :param identifiant: ID from lot table
    :type identifiant: str

    :rtype: GeneralMessage
    """
    try:
        stmt = FeatureType.__table__.delete().where(FeatureType.id == identifiant)
        db.session.execute(stmt)
        db.session.flush()
        
    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    mess = "Les enregistrements dans la table feature_type liés au lot {} ont été effacés".format(identifiant)
    return jsonify(message=mess), 200


def delete_suivi_prod_lot_id(identifiant, cascade=None):  # noqa: E501
    """delete_suivi_prod_lot_id

    Delete a record in Lot table. # noqa: E501

    :param identifiant: 
    :type identifiant: str

    :rtype: GeneralMessage
    """
    try:
        lot = Lot.query.filter(Lot.id == identifiant).one()
        
        if cascade == True:
            delete_suivi_prod_featuretype_id(lot.id)

            ut = UniteTravail2.query.filter(UniteTravail2.id_lot == lot.id).all()
            for v in ut:
                delete_suivi_prod_unite_travail_id(v.id, True)

        db.session.delete(lot)
        db.session.flush()

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))    

    mess = "Le lot {} a été effacé de la table Lot. Option casde = {}".format(lot.id, cascade)
    return jsonify(message=mess), 200


def delete_suivi_prod_unite_travail_id(identifiant, cascade=None):  # noqa: E501
    """delete_suivi_prod_unite_travail_id

    Delete a record in table unite_travail_2. # noqa: E501

    :param identifiant: Work area id
    :type identifiant: str

    :rtype: GeneralMessage
    """
    try:
        ut = UniteTravail2.query.filter(UniteTravail2.id == identifiant).one()

        if cascade == True:
            stmt = EtapeUt.__table__.delete().where(EtapeUt.id_unite_travail == ut.id)
            db.session.execute(stmt)            
            
        db.session.delete(ut)
        db.session.flush()

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    mess = "L'unité de travail {} a été effacé de la table unite_travail_2. Option casde = {}".format(ut.id, cascade)
    return jsonify(message=mess), 200


def get_suivi_prod_code_list(ident=None, nom=None):  # noqa: E501
    """get_suivi_prod_code_list

    Obtient un enregistrement de la table suivi_prod.list_codes. # noqa: E501

    :param id: 
    :type id: str
    :param nom: 
    :type nom: str

    :rtype: List[SuiviProdCodeList]
    """
    try:
        if nom != None:        
            codes = ListeCode.query.filter(ListeCode.nom == nom).all()
        elif ident != None:
            codes = ListeCode.query.filter(ListeCode.id == ident).all()
        else:
            codes = ListeCode.query.all()
                
        MASerializer = ListeCodeSchema()
        liste_codes = []
        for v in codes:
            liste_codes.append(MASerializer.dump(v))

    except NoResultFound as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    return jsonify(liste_codes), 200
    

def get_suivi_prod_codes(categorie=None, nom=None, ident=None, id_list_codes=None):  # noqa: E501
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
    try:
        if nom != None:        
            codes = Code.query.filter(Code.nom == nom).all()
        elif id_list_codes != None:
            codes = Code.query.filter(Code.id_liste_codes == id_list_codes).all()
        elif ident != None:
            codes = Code.query.filter(Code.id == ident).all()
        else:
            raise Exception(utils_gapi.message_erreur(erreurs.GAPIAllParametersEndPointAreNull(), 400))
                
        MASerializer = CodeSchema()
        liste_codes = []
        for v in codes:
            liste_codes.append(MASerializer.dump(v))

    except NoResultFound as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    return jsonify(liste_codes), 200


def get_suivi_prod_codes_code(code):  # noqa: E501
    """get_suivi_prod_codes_code

     # noqa: E501

    :param code: 
    :type code: str

    :rtype: SuiviProdCode
    """
    # Requête dans la table de Code
    try:
        if str(code).isdigit():
            res = Code.query.filter(Code.id == code).one()
        else:
            res = Code.query.filter(Code.nom == code).one()        

        MASerializer = CodeSchema()
        code_json = MASerializer.dump(res)
    
    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))    
    
    return jsonify(code_json), 200


def get_suivi_prod_etape_ut_id(identifiant):  # noqa: E501
    """Your GET endpoint

    Retrieve a record from etape_ut table. # noqa: E501

    :param identifiant: 
    :type identifiant: str

    :rtype: SuiviProdEtapeUt
    """
    # Requête dans la table de Etape_ut
    try:
        res = EtapeUt.query.filter(EtapeUt.id == identifiant).one()
        MASerializer = EtapeUtSchema()
        etape_ut_json = MASerializer.dump(res)
    
    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    return jsonify(etape_ut_json), 200


def get_suivi_prod_featuretype_id(identifiant):  # noqa: E501
    """Your GET endpoint

    Retreive a record from feature)type table. # noqa: E501

    :param identifiant: ID from lot table
    :type identifiant: str

    :rtype: List[SuiviProdFeaturetype]
    """
    # Requête dans la table de featuretype
    try:
        list_feat = []
        res = FeatureType.query.filter(FeatureType.id == identifiant).all()
        for v in res:
            list_feat.append(v.as_dict())
    
        rcoll = {}
        rcoll["RecordCollection"] = list_feat

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))    
    
    return jsonify(rcoll), 200


def get_suivi_prod_lot_id(identifiant, full_relation=None):  # noqa: E501
    """get_suivi_prod_lot_id

    Retrieve a record from Lot table. By using the parameter full_relation&#x3D;False you can retreive only the Lot record or by using full_relation&#x3D;True you can retreive the Lot and all its dependencies (related table records). # noqa: E501

    :param identifiant: 
    :type identifiant: str
    :param full_relation: 
    :type full_relation: Boolean

    :rtype: InlineResponse2001
    """
    # Requête dans la table de lot
    try:
        lot = Lot.query.filter(Lot.id == identifiant).one()
        
    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    if full_relation == False: # Retourne le lot sans ses relations        
        return jsonify(lot.as_dict()), 200
    else:
        try:
            # Boucle pour construire la liste des unité de travail reliées au lot
            liste_ut = []
            resultats = UniteTravail2.query.filter(UniteTravail2.id_lot == lot.id).all()
            for v in resultats:
                rep = get_suivi_prod_unite_travail_id(v.id, True)                
                liste_ut.append(rep[0].json)

            # Boucle pour construire la liste des featuretype reliés au lot
            liste_feat = []
            res = FeatureType.query.filter(FeatureType.id == lot.id).all()
            for v in res:
                liste_feat.append(v.as_dict())

            # Construction de la réponse soit le lot + toutes ses dépendances
            full = {}
            full["lot"] = lot.as_dict()
            full["executant"] = ""
            full["relations"] = {"unite_travail_2": liste_ut, "feature_type": liste_feat}
            
            return jsonify(full), 200

        except NoResultFound as e:
            raise Exception(utils_gapi.message_erreur(e, 400))

    
def get_suivi_prod_unite_travail_id(identifiant, full_relation=None):  # noqa: E501
    """get_suivi_prod_unite_travail_id

    Retourne un enregistrement de la table suivi-prod.unite_travail_2. En utilisant le 
    paramètre full_relation=False vous obtener uniquement l'enregistrement de la table suivi-prod.unite_travail_2. 
    En utilisant le paramètre full_relation=True vous obtenez l'enregistrement de la table suivi-prod.unite_travail_2
    ainsi que toutes ses dépendances (l'information provenant des tables en relation).

    :param identifiant: Identifiant de l'unité de travail
    :type identifiant: str
    :param full_relation: 
    :type full_relation: bool

    :rtype: InlineResponse200
    """
    # Requête dans la table de unite_travail_2
    try:
        ut = UniteTravail2.query.filter(UniteTravail2.id == identifiant).one()
        
    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    if full_relation == False: # Retourne l'unité de travail sans ses relations
        return jsonify(ut.as_dict()), 200
    else:
        try:
            # Boucle pour construire la liste des étapes reliées à l'unité de travail
            list_etape_ut = []
            res = EtapeUt.query.filter(EtapeUt.id_unite_travail == ut.id).all()
            for v in res:
                list_etape_ut.append(v.as_dict())
            
            # Construction de la réponse soit l'unité de travail + toutes ses dépendances
            full = {}
            full["unite_travail_2"] = ut.as_dict()        
            full["relations"] = {"etape_ut": list_etape_ut, "sous_etape_travail": ""}

            return jsonify(full), 200

        except NoResultFound as e:
            raise Exception(utils_gapi.message_erreur(e, 400))


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

    try:
        ut = UniteTravail2.query.join(Lot).filter(Lot.theme_cl == theme) \
                                          .filter(Lot.statut_lot_cl.in_([10001, 10002])).all()
        
        liste_ut = []
        for v in ut:
            liste_ut.append(v.id)

        ret = GeneralListeValeur(value=liste_ut)        

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    return jsonify(ret.to_dict()), 200


def get_suivi_prod_type_travail_theme(theme):  # noqa: E501
    """Your GET endpoint

    Retourne une liste des travaux disponibles pour un thème donné. # noqa: E501

    :param theme: 
    :type theme: str

    :rtype: List[SuiviProdCode]
    """
    try:
        co = get_suivi_prod_codes_code(theme)
        
        codes = Code.query.filter(Code.id_liste_codes == 10800) \
                         .filter(Code.nom.like(str(co[0].json["nom"])+'%')).all()
        
        MASerializer = CodeSchema()
        liste_codes = []
        for v in codes:
            liste_codes.append(MASerializer.dump(v))

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    return jsonify(liste_codes), 200


def post_suivi_prod_requete_bd(body=None, output_format=None, simplifier=None):  # noqa: E501
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
            raise Exception(utils_gapi.message_erreur(erreurs.GAPIInvalidJSONPayload(), 400))            
        
        # On s'assure qu'il n'y a pas de ";" à la fin de la requête SQL envotée par l'usager
        body.sql = str(body.sql).strip(";")

        #TODO: Vérifier que la requête SQL ne contient pas de INSERT, UPDATE, DELETE, ALTER, TRUNCATE, etc.

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
            raise Exception(utils_gapi.message_erreur(erreurs.GAPIUnknownOutputFormat(output_format), 400))
        
        # Lancement de la requête de l'usager vers la BD
        row = db_view_session.execute(text(sql_template)).fetchone()    
        
        return jsonify(row[0]), 200

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 500))            

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

    except Exception as e:
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
            
    except Exception as e:
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

    except Exception as e:        
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

        #conversion de la géométrie en EWKT. C'est parce que GeoAlchemy aime ça de même!
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

    except Exception as e:        
        raise Exception(utils_gapi.message_erreur(e, 400))
    
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

        db.session.flush()        

        # Serializer le contenu de l'objet BD en JSON pour le retourner
        MASerializer = EtapeUtSchema()
        e_ut = MASerializer.dump(rs)        

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

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

        db.session.flush()

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
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

        db.session.flush()

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    return jsonify(rs.as_dict()), 200
