from flask import g

MessageDict = {
                "GAPIInvalidPassword": 
                    {"fr": "Le mot de passe est invalide",
                     "en": "Invalid password"},

                "GAPIInvalidUserName": 
                    {"fr": "L'usager n'existe pas",
                     "en": "User does not exist"},

                "GAPIInvalidS3URL": 
                    {"fr": "Le URL: {} n'existe pas",
                     "en": "URL: {} does not exist"},

                "GAPIAllParametersEndPointAreNull": 
                    {"fr": "Tous les paramètres de l'appel sont null",
                     "en": "All endpoint parameters are null"},

                "GAPIInvalidJSONPayload": 
                    {"fr": "Le JSON attendu par le service est invalide",
                     "en": "The JSON expected by the service is invalid"},

                "GAPIUnknownOutputFormat": 
                    {"fr": "Le format de sortie: {} est inconnu",
                     "en": "Output format: {} is unknown"},

                "GAPIInvalidGeometry": 
                    {"fr": "Géométrie invalide: {}",
                     "en": "Invalid geometry: {}"},

                "GAPIMultiPolygonNotAllowed": 
                    {"fr": "Les multipolygones ne sont pas acceptés. Votre géométrie contient {} polygones",
                     "en": "Multipolygons are not allowed. Your geometry contains {} polygons"},

                "GAPIThemeURLAccessNotAllowed": 
                    {"fr": "Le thème référencé dans le url: {} ne figure pas dans la liste des thèmes de l'utilisateur. Les thèmes autorisée sont: {}",
                     "en": "The theme referenced in the url: {} is not in the user's theme list. Themes allowed are: {}"}
              }

class GAPIError(Exception):
    """Base class for other exceptions"""
    def __init__(self, *args):
        self.args = []
        if args:
            self.args = args

    def __str__(self):
        if len(self.args) > 0:
            message = MessageDict[self.__class__.__name__][g.user_lang]
            for arg in self.args:
                message = message.replace("{}", arg, 1)

            return message

        else:
            return MessageDict[self.__class__.__name__][g.user_lang]

class GAPIInvalidUserName(GAPIError):
    """Nom d'usager inconnu"""
    pass

class GAPIInvalidPassword(GAPIError):
    """Mot de passe invalide"""
    pass

class GAPIInvalidS3URL(GAPIError):
    """Le URL n'existe pas dans S3"""
    pass

class GAPIAllParametersEndPointAreNull(GAPIError):
    """Tous les paramètres d'un appel à l'API sont null"""
    pass

class GAPIInvalidJSONPayload(GAPIError):
    """Le JSON passé en paramètre (payload) est invalide"""
    pass

class GAPIUnknownOutputFormat(GAPIError):
    """Le format de sortie ne figure pas dans les options"""
    pass

class GAPIInvalidGeometry(GAPIError):
    """Géométrie invalide"""
    pass

class GAPIMultiPolygonNotAllowed(GAPIError):
    """Les poygones multiples ne sont pas acceptés"""
    pass

class GAPIThemeURLAccessNotAllowed(GAPIError):
    """L'usager n'a pas accès au url pour un thème spécifique"""
    pass