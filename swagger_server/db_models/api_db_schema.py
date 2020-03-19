# coding: utf-8
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
from swagger_server.config import db, ma
from marshmallow import fields

db.Model.metadata = MetaData(schema="jmp_api")

class CleAw(db.Model):
    __tablename__ = 'cle_aws'

    id = db.Column(db.String(50), primary_key=True, index=True)
    acces_id = db.Column(db.String(50))
    acces_secret = db.Column(db.String(50))
    desc = db.Column(db.String(256))

class CleAwSchema(ma.ModelSchema):
    class Meta:
        model = CleAw
        sqla_session = db.session


class LienUsagerEquipe(db.Model):
    __tablename__ = 'lien_usager_equipe'

    id = db.Column(db.String(50), primary_key=True, index=True)
    nom_usager = db.Column(db.ForeignKey('usager.nom_usager'))    
    code_id = db.Column(db.Integer)
    
class LienUsagerEquipeSchema(ma.ModelSchema):
    class Meta:
        model = LienUsagerEquipe
        sqla_session = db.session


class LienUsagerScope(db.Model):
    __tablename__ = 'lien_usager_scope'

    id = db.Column(db.String(50), primary_key=True, index=True)
    nom_usager = db.Column(db.ForeignKey('usager.nom_usager'))
    code_id = db.Column(db.Integer)
    
class LienUsagerScopeSchema(ma.ModelSchema):
    class Meta:
        model = LienUsagerScope
        sqla_session = db.session


class LienUsagerTheme(db.Model):
    __tablename__ = 'lien_usager_theme'

    id = db.Column(db.String(50), primary_key=True, index=True)
    nom_usager = db.Column(db.ForeignKey('usager.nom_usager'))
    code_id = db.Column(db.Integer, nullable=False)
    
class LienUsagerThemeSchema(ma.ModelSchema):
    class Meta:
        model = LienUsagerTheme
        sqla_session = db.session

class Usager(db.Model):
    __tablename__ = 'usager'

    nom_usager = db.Column(db.String(50), primary_key=True, index=True)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    cle_aws_id = db.Column(db.ForeignKey('cle_aws.id'))

    cle_aws = relationship('CleAw', primaryjoin='Usager.cle_aws_id == CleAw.id')
    scope = relationship('LienUsagerScope', primaryjoin='Usager.nom_usager == LienUsagerScope.nom_usager')
    theme = relationship('LienUsagerTheme', primaryjoin='Usager.nom_usager == LienUsagerTheme.nom_usager')
    equipe = relationship('LienUsagerEquipe', primaryjoin='Usager.nom_usager == LienUsagerEquipe.nom_usager')
    

class UsagerSchema(ma.ModelSchema):    
    ordered = False
    
    class Meta:
        model = Usager
        sqla_session = db.session
    
    cle_aws = fields.Nested('CleAwSchema', many=False)
    scope = fields.Pluck('LienUsagerScopeSchema', 'code_id', many=True)
    theme = fields.Pluck('LienUsagerThemeSchema', 'code_id', many=True)
    equipe = fields.Pluck('LienUsagerEquipeSchema', 'code_id', many=True)
