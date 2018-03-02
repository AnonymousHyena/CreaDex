from db_setup import *
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///pedia.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


if __name__ == '__main__':
    session.query(Creature).delete()
    session.query(DamageType).delete()
    session.query(Attribute).delete()
    session.query(Encounter).delete()

    damage = DamageType()
    damage.name = "Acid"
    damage.desc = "The corrosive spray of a black dragon's breath and the dissolving enzymes secreted by a black pudding deal acid damage"
    session.add(damage)
    damage = DamageType()
    damage.name = "Bludgeoning"
    damage.desc = "Blunt force attacks-hammers, falling, constriction, and the like-deal bludgeoning damage"
    session.add(damage)
    damage = DamageType()
    damage.name = "Cold"
    damage.desc = "The infernal chill radiating from an ice devil's spear and the frigid blast of a white dragon's breath deal cold damage"
    session.add(damage)
    damage = DamageType()
    damage.name = "Fire"
    damage.desc = "Red dragons breath fire, and many spells conjure flames to deal fire damage"
    session.add(damage)
    damage = DamageType()
    damage.name = "Force"
    damage.desc = "Force is pure magical energy focused into a damaging form. Most effects that deal force damage are spells, inclding magic missile and spiritual weapon"
    session.add(damage)
    damage = DamageType()
    damage.name = "Lightning"
    damage.desc = "A lightning bolt spell and a blue dragon's breath deal lightning damage"
    session.add(damage)
    damage = DamageType()
    damage.name = "Necrotic"
    damage.desc = "Necrotic damage, dealt by certain undead and a spell such as chill touch, withers matter and even the soul"
    session.add(damage)
    damage = DamageType()
    damage.name = "Piercing"
    damage.desc = "Puncturing and impaling attacks, including spears and monster' bites, deal piercing damage"
    session.add(damage)
    damage = DamageType()
    damage.name = "Poison"
    damage.desc = "Venomous stings and the toxic gas of a green dragon's breath deal poison damage"
    session.add(damage)
    damage = DamageType()
    damage.name = "Psychic"
    damage.desc = "Mental abilities such as a mind flayer's psionic blast deal psychic damage"
    session.add(damage)
    damage = DamageType()
    damage.name = "Radiant"
    damage.desc = "Radiant damage, dealt by a cleric's flame strike spell or an angel's smiting weapon, sears the flesh like fire and overloads the spirit with power"
    session.add(damage)
    damage = DamageType()
    damage.name = "Slashing"
    damage.desc = "Swords, axes, and monsters' claws deal slashing damage"
    session.add(damage)
    damage = DamageType()
    damage.name = "Thunder"
    damage.desc = "A consecutive burst of sound, such as the effect of the thunderwave spell, deals thunder damage"
    session.add(damage)
    damage = DamageType()
    damage.name = "non-Silver"
    damage.desc = "Bludgeoning, piercing and slashing form non-silver weapons"
    session.add(damage)
    damage = DamageType()
    damage.name = "non-Magic"
    damage.desc = "Bludgeoning, piercing and slashing form non-magical weapons"
    session.add(damage)
    damage = DamageType()
    damage.name = "non-Adamantine"
    damage.desc = "Bludgeoning, piercing and slashing form non-adamantine weapons"
    session.add(damage)

    attr = Attribute()
    attr.name = "Keen Smell"
    attr.desc = "It has advantage on Wisdom (Perception) checks that rely on smell"
    session.add(attr)

    creature = Creature()
    creature.name = "Rat"
    creature.size = "Tiny"
    creature.speed = 20
    creature.numAttacks = 1
    creature.dmgTypes = [session.query(DamageType).filter_by(name="Piercing").one()]
    creature.attributes = [session.query(Attribute).filter_by(name="Keen Smell").one()]
    creature.notes = "A common rat, found in almost any city in the world"
    session.add(creature) 
    creature = Creature()
    creature.name = "Riding Horse"
    creature.size = "Large"
    creature.speed = 60
    creature.numAttacks = 1
    creature.dmgTypes = [session.query(DamageType).filter_by(name="Bludgeoning").one()]
    creature.notes = "A common horse used for riding, found in almost any city in the world"
    session.add(creature)

    session.commit()