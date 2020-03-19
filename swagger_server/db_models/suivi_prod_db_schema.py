# coding: utf-8
#from sqlalchemy import db.Column, ForeignKey, ForeignKeyConstraint, Integer, Numeric, db.String, MetaData

from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship

from geoalchemy2.types import Geometry
from geoalchemy2.shape import to_shape
from shapely_geojson import dumps, Feature
from swagger_server.controllers import utils_gapi
import shapely.wkt
import json
import os

#from sqlalchemy.ext.declarative import declarative_base
from swagger_server.config import db, ma

from marshmallow_sqlalchemy import TableSchema

#db.Model = declarative_base()
db.Model.metadata = MetaData(schema="jmp")

#db.metadata = MetaData(schema="jmp")

class ListeCode(db.Model):
    __tablename__ = 'liste_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    desc_en = db.Column(db.String(200))
    desc_fr = db.Column(db.String(200))

class ListeCodeSchema(ma.ModelSchema):
    class Meta:
        model = ListeCode
        sqla_session = db.session


class Code(db.Model):
    __tablename__ = 'code'

    id = db.Column(db.Integer, primary_key=True)
    id_liste_codes = db.Column(db.ForeignKey('liste_codes.id'))
    nom = db.Column(db.String(50))
    desc_en = db.Column(db.String(200))
    desc_fr = db.Column(db.String(200))

    liste_code = relationship('ListeCode')

class CodeSchema(ma.ModelSchema):
    class Meta:
        model = Code
        sqla_session = db.session

class Lot(db.Model):
    __tablename__ = 'lot'

    etampe = db.Column(db.String(50))
    dt_c = db.Column(db.String(30))
    dt_m = db.Column(db.String(30))
    id = db.Column(db.String(64), primary_key=True)
    operateur = db.Column(db.String(100))
    date_debut = db.Column(db.String(20))
    date_fin = db.Column(db.String(20))
    theme_cl = db.Column(db.ForeignKey('code.id'))
    type_travail_cl = db.Column(ForeignKey('code.id'))
    statut_lot_cl = db.Column(ForeignKey('code.id'))

    code = relationship('Code', primaryjoin='Lot.statut_lot_cl == Code.id')
    code1 = relationship('Code', primaryjoin='Lot.theme_cl == Code.id')
    code2 = relationship('Code', primaryjoin='Lot.type_travail_cl == Code.id')
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UniteTravail2(db.Model):
    __tablename__ = 'unite_travail_2'

    etampe = db.Column(db.String(50))
    dt_c = db.Column(db.String(30))
    dt_m = db.Column(db.String(30))
    id = db.Column(db.String(64), primary_key=True)
    id_lot = db.Column(ForeignKey('lot.id'))
    date_prevue_fin = db.Column(db.String(20))
    date_debut = db.Column(db.String(20))
    date_fin = db.Column(db.String(20))
    where_clause = db.Column(db.String(1000))
    shape = db.Column(Geometry(geometry_type='POLYGON', srid=4617, dimension=2))

    lot = relationship('Lot')

    def as_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d["shape"] = utils_gapi.convert_whatever_to_geojson(d["shape"])

        return d

class FeatureType(db.Model):
    __tablename__ = 'feature_type'

    etampe = db.Column(db.String(50))
    dt_c = db.Column(db.String(30))
    dt_m = db.Column(db.String(30))
    id = db.Column(db.String(64), primary_key=True, nullable=False)
    local_name = db.Column(db.String(50), primary_key=True, nullable=False)
    spatial_repres_type_pna = db.Column(ForeignKey('code.id'))

    code = relationship('Code')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class EtapeUt(db.Model):
    __tablename__ = 'etape_ut'

    etampe = db.Column(db.String(50))
    dt_c = db.Column(db.String(30))
    dt_m = db.Column(db.String(30))
    id = db.Column(db.String(64), primary_key=True)
    id_unite_travail = db.Column(ForeignKey('unite_travail_2.id'))    
    nom_etape_cl = db.Column(ForeignKey('code.id'))    
    description = db.Column(db.String(200))
    operateur = db.Column(db.String(100))
    date_debut = db.Column(db.String(20))
    date_fin = db.Column(db.String(20))
    statut_etape_cl = db.Column(ForeignKey('code.id'))    

    unite_travail_2 = relationship('UniteTravail2')
    code = relationship('Code', primaryjoin='EtapeUt.nom_etape_cl == Code.id')
    code1 = relationship('Code', primaryjoin='EtapeUt.statut_etape_cl == Code.id')

class EtapeUtSchema(TableSchema):
    class Meta:
        include_fk = True
        table = EtapeUt.__table__
        strict = True
        sqla_session = db.session
    
"""
class Contractant(db.Model):
    __tablename__ = 'contractant'

    etampe = db.Column(db.String(50))
    dt_c = db.Column(db.String(30))
    dt_m = db.Column(db.String(30))
    id = db.Column(db.String(64), primary_key=True)
    nom = db.Column(db.String(100))
    adresse = db.Column(db.String(200))
    courriel = db.Column(db.String(100))
    statut_contractant_cl = db.Column(ForeignKey('code.id'))

    code = relationship('Code')


class Executant(db.Model):
    __tablename__ = 'executant'

    etampe = db.Column(db.String(50))
    dt_c = db.Column(db.String(30))
    dt_m = db.Column(db.String(30))
    id = db.Column(ForeignKey('lot.id'), db.ForeignKey('contractant.id'), primary_key=True)
    id_contractant = db.Column(db.String(64))
    no_contrat = db.Column(db.String(64))
    prix_contrat = db.Column(Numeric(38, 8))

    lot = relationship('Lot', uselist=False)

class SousUniteTravail(db.Model):
    __tablename__ = 'sous_unite_travail'

    etampe = db.Column(db.String(50))
    dt_c = db.Column(db.String(30))
    dt_m = db.Column(db.String(30))
    id = db.Column(db.String(64), primary_key=True, nullable=False)
    id_unite_travail = db.Column(ForeignKey('unite_travail_2.id'), primary_key=True, nullable=False)
    date_prevue_fin = db.Column(db.String(20))
    date_debut = db.Column(db.String(20))
    date_fin = db.Column(db.String(20))

    unite_travail_2 = relationship('UniteTravail2')


class EtapeSut(db.Model):
    __tablename__ = 'etape_sut'
    __table_args__ = (
        ForeignKeyConstraint(['id_sous_unite_travail', 'id_unite_travail'], ['sous_unite_travail.id', 'sous_unite_travail.id_unite_travail']),
    )

    etampe = db.Column(db.String(50))
    dt_c = db.Column(db.String(30))
    dt_m = db.Column(db.String(30))
    id = db.Column(db.String(64), primary_key=True)
    id_sous_unite_travail = db.Column(db.String(64))
    id_unite_travail = db.Column(db.String(64))
    description = db.Column(db.String(200))
    operateur = db.Column(db.String(100))
    nom_etape_cl = db.Column(ForeignKey('code.id'))
    date_debut = db.Column(db.String(20))
    date_fin = db.Column(db.String(20))
    statut_etape_cl = db.Column(ForeignKey('code.id'))

    sous_unite_travail = relationship('SousUniteTravail')
    code = relationship('Code', primaryjoin='EtapeSut.nom_etape_cl == Code.id')
    code1 = relationship('Code', primaryjoin='EtapeSut.statut_etape_cl == Code.id')

"""