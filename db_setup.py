# Standard Configuration for SQLAlchemy 
import sys
import os

from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# End of Standard Configuration

creature_damageType_res = Table('creature_damageType_res',Base.metadata,
    Column('creature_id',Integer,ForeignKey('creature.id')),
    Column("damageType_id",Integer,ForeignKey('damageType.id')),
    UniqueConstraint('creature_id', 'damageType_id', name='UC_creature_id_damageType_id'))

creature_damageType_imm = Table('creature_damageType_imm',Base.metadata,
    Column('creature_id',Integer,ForeignKey('creature.id')),
    Column("damageType_id",Integer,ForeignKey('damageType.id')),
    UniqueConstraint('creature_id', 'damageType_id', name='UC_creature_id_damageType_id'))


creature_damageType_dmg = Table('creature_damageType_dmg',Base.metadata,
    Column('creature_id',Integer,ForeignKey('creature.id')),
    Column("damageType_id",Integer,ForeignKey('damageType.id')),
    UniqueConstraint('creature_id', 'damageType_id', name='UC_creature_id_damageType_id'))


creature_damageType_vul = Table('creature_damageType_vul',Base.metadata,
    Column('creature_id',Integer,ForeignKey('creature.id')),
    Column("damageType_id",Integer,ForeignKey('damageType.id')),
    UniqueConstraint('creature_id', 'damageType_id', name='UC_creature_id_damageType_id'))


attribute_creature = Table('attribute_creature',Base.metadata,
    Column('creature_id',Integer,ForeignKey('creature.id')),
    Column("attribute_id",Integer,ForeignKey('attribute.id')))

class Creature(Base):
    __tablename__ = 'creature'

    id = Column(Integer, primary_key = True)
    name = Column(String(25), nullable = False, unique= True)
    size = Column(String(12))
    speed = Column(Integer)
    vulnerabilities = relationship("DamageType", secondary = creature_damageType_vul)
    resistances = relationship("DamageType", secondary = creature_damageType_res)
    immunities = relationship("DamageType", secondary = creature_damageType_imm)
    spells = Column(String(500))
    attributes = relationship("Attribute", secondary = attribute_creature)
    numAttacks = Column(Integer)
    dmgTypes = relationship("DamageType", secondary = creature_damageType_dmg)
    notes = Column(String(700))
    encounters = relationship("Encounter", cascade = 'all,delete', lazy='dynamic')

class DamageType(Base):
    __tablename__ = 'damageType'

    id = Column(Integer, primary_key = True)
    name = Column(String(30), nullable = False, unique= True)
    desc = Column(String(150), unique= True)

class Attribute(Base):
    __tablename__ = 'attribute'

    id = Column(Integer, primary_key = True)
    name = Column(String(20), nullable = False, unique= True)
    desc = Column(String(350), unique= True)

class Encounter(Base):
    __tablename__ = 'encounter'

    id = Column(Integer, primary_key = True)
    creature_id = Column(Integer, ForeignKey('creature.id'), nullable=False)
    hitsLand = Column(Integer, nullable = False) #evasion
    atksLand = Column(Integer, nullable = False) #evasion
    dmgLand = Column(Integer, nullable = False) #HP
    atkBonus = Column(Integer, nullable = False) 
    hitsRec = Column(Integer, nullable = False) #accuracy
    atksRec = Column(Integer, nullable = False) #accuracy
    dmgRec = Column(Integer, nullable = False) #dmgAverage
    ac = Column(Integer, nullable = False)

class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key = True)
    name = Column(String(15), nullable=False)
    ac = Column(Integer, nullable = False)
    atkBonus = Column(Integer, nullable = False)
        

engine = create_engine('sqlite:///pedia.db')

Base.metadata.create_all(engine)
