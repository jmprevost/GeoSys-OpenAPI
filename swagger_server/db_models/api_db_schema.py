# coding: utf-8
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
from swagger_server.config import db, ma
from marshmallow import fields

from sqlalchemy.ext.associationproxy import association_proxy

db.Model.metadata = MetaData(schema="jmp_api")

class CleAw(db.Model):
    __tablename__ = 'cle_aws'

    id = db.Column(db.String(50), primary_key=True, index=True)
    acces_id = db.Column(db.String(50))
    acces_secret = db.Column(db.String(50))
    desc = db.Column(db.String(256))

    def __repr__(self):
        return str(self.id)

class CleAwSchema(ma.ModelSchema):
    class Meta:
        model = CleAw
        sqla_session = db.session

# Tables de liens pour la relation many-to-many entre usager_geosys
# et les vues créées à partir de la table de code du suivi de production 
l_usager_equipe = db.Table('l_usager_equipe',
    db.Column('usager_id', db.Integer, db.ForeignKey('usager_geosys.usager_id')),
    db.Column('code_id', db.Integer, db.ForeignKey('v_codes_equipes.id'))
)

l_usager_scope = db.Table('l_usager_scope',
    db.Column('usager_id', db.Integer, db.ForeignKey('usager_geosys.usager_id')),
    db.Column('code_id', db.Integer, db.ForeignKey('v_codes_scopes.id'))
)

l_usager_theme = db.Table('l_usager_theme',
    db.Column('usager_id', db.Integer, db.ForeignKey('usager_geosys.usager_id')),
    db.Column('code_id', db.Integer, db.ForeignKey('v_codes_themes.id'))
)

# Vues créées à partir de la table code du suivi de production.
# Ce sont des sous-ensembles des thèmes, scopes et équipes
class v_CodesThemes(db.Model):
    __table__ = db.Table('v_codes_themes', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('id_liste_codes', db.Integer),
    db.Column('nom', db.String(50)),
    db.Column('desc_en', db.String(200)),
    db.Column('desc_fr', db.String(200)),
        autoload=True, autoload_with=db.get_engine()
    )

    def __repr__(self):
        return str("{}-{}".format(self.id, self.nom))

class v_CodesScopes(db.Model):
    __table__ = db.Table('v_codes_scopes', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('id_liste_codes', db.Integer),
    db.Column('nom', db.String(50)),
    db.Column('desc_en', db.String(200)),
    db.Column('desc_fr', db.String(200)),
        autoload=True, autoload_with=db.get_engine()
    )

    def __repr__(self):
        return str("{}-{}".format(self.id, self.nom))

class v_CodesEquipes(db.Model):
    __table__ = db.Table('v_codes_equipes', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('id_liste_codes', db.Integer),
    db.Column('nom', db.String(50)),
    db.Column('desc_en', db.String(200)),
    db.Column('desc_fr', db.String(200)),
        autoload=True, autoload_with=db.get_engine()
    )

    def __repr__(self):
        return str("{}-{}".format(self.id, self.nom))

# Définition de la table des usager geosys
class UsagerGeosys(db.Model):
    __tablename__ = 'usager_geosys'
    usager_id = db.Column(db.Integer, primary_key=True)    
    nom_usager = db.Column(db.String(50), unique=True)
    mot_de_passe = db.Column(db.String(300), unique=True)
    cle_aws_id = db.Column(db.ForeignKey('cle_aws.id'))
    themes = db.relationship("v_CodesThemes", secondary=l_usager_theme)
    scopes = db.relationship("v_CodesScopes", secondary=l_usager_scope)
    equipes = db.relationship("v_CodesEquipes", secondary=l_usager_equipe)
    cle_aws = db.relationship('CleAw', primaryjoin='UsagerGeosys.cle_aws_id == CleAw.id')

class UsagerGeosysSchema(ma.ModelSchema):    
    ordered = False
    
    class Meta:
        model = UsagerGeosys
        sqla_session = db.session
    
    cle_aws = fields.Nested('CleAwSchema', many=False)
    scope = fields.Pluck('v_CodesScopes', 'code_id', many=True)
    theme = fields.Pluck('v_CodesThemes', 'code_id', many=True)
    equipe = fields.Pluck('v_CodesEquipes', 'code_id', many=True)