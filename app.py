from db_setup import *
from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, exc

from gtts import gTTS
import os
import random
import string

engine = create_engine('sqlite:///pedia.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/profiles')
def profiles():
	pr = session.query(Profile).all()
	return render_template('Profiles/index.html', list=pr)

@app.route('/profiles/<prof>')
def profile(prof):
	if 'name' in login_session:
		del login_session['name']
        del login_session['atkBonus']
        del login_session['ac']
	pr = session.query(Profile).filter_by(id=prof).one()
	login_session['name'] = pr.name
	login_session['atkBonus'] = pr.atkBonus
	login_session['ac'] = pr.ac
	return redirect(url_for('creatures'))


@app.route('/profiles/new')
def newProfile():
	return render_template('Profiles/form.html')

@app.route('/profiles/create', methods=['POST'])
def createProfile():
	prof = Profile()
	prof.name = format(request.form['name'])
	prof.atkBonus = format(request.form['atkBonus'])
	prof.ac = format(request.form['ac'])
	try:
		session.add(prof)
		session.commit()
		return redirect(url_for('profiles'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Profiles/form.html', error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@app.route('/profiles/delete/<prof>')
def deleteProfile(prof):
	session.query(Profile).filter_by(id=prof).delete()
	session.commit()
	return redirect(url_for('profiles'))

@app.route('/creatures')
def creatures():
	cr = session.query(Creature).all()
	return render_template('Creatures/index.html', list=cr)

@app.route('/creatures/<crea>')
def showCreature(crea):
	cr = session.query(Creature).filter_by(id=crea).one()
	staf = {'evasion':0, 'dps':0, 'acc':0, 'hp':1000 }
	ammount = [0,0,0]
	for encounter in cr.encounters:
		if encounter.atksLand != 0:
			staf['evasion'] += float((1-(float(encounter.hitsLand)/float(encounter.atksLand)))*20+float(encounter.atkBonus))
			ammount[0] +=1
		if encounter.atksRec != 0:
			staf['acc'] += float(encounter.ac)-float((1-(float(encounter.hitsRec)/float(encounter.atksRec)))*20)
			ammount[2] +=1
		if staf['hp'] > encounter.dmgLand and encounter.dmgLand>0:
			staf['hp'] = encounter.dmgLand
		if encounter.hitsRec != 0:
			staf['dps'] += float(encounter.dmgRec)/float(encounter.hitsRec)
			ammount[1] +=1
	if ammount[0]>0:
		staf['evasion'] = round(float(staf['evasion']/ammount[0]),3)
		if 'atkBonus' in login_session:
			staf['evasion'] = (staf['evasion']-login_session['atkBonus'])*5
			if staf['evasion']<0:
				staf['evasion'] = 0
	if ammount[1]>0:
		staf['dps'] = round(float(staf['dps']/ammount[1]), 3)
	if ammount[2]>0:
		staf['acc'] = round(float(staf['acc']/ammount[2]), 3)
		if 'ac' in login_session:
			staf['acc'] = 100-(login_session['ac']-staf['acc'])*5
			if staf['acc']<0:
				staf['acc'] = 0
	if staf['hp']==1000:
		staf['hp']='?'

	return render_template('Creatures/show.html', cr=cr, st=staf)

@app.route('/attributes')
def attributes():
	attr = session.query(Attribute).all()
	return render_template('Attributes/index.html', list=attr)

@app.route('/attributes/new')
def newAttribute():
	return render_template('Attributes/form.html')

@app.route('/attributes/create', methods=['POST'])
def createAttribute():
	attr = Attribute()
	attr.name = format(request.form['name'])
	attr.desc = format(request.form['desc'])
	try:
		session.add(attr)
		session.commit()
		return redirect(url_for('attributes'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Attributes/form.html', error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@app.route('/attributes/edit/<attr>')
def editAttribute(attr):
	at = session.query(Attribute).filter_by(id=attr).one()
	return render_template('Attributes/form.html', at=at)

@app.route('/attributes/update/<attr>', methods=['POST'])
def updateAttribute(attr):
	at = session.query(Attribute).filter_by(id=attr).one()
	at.name = format(request.form['name'])
	at.desc = format(request.form['desc'])
	try:
		session.commit()
		return redirect(url_for('attributes'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Attributes/form.html', at=at, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@app.route('/attributes/delete/<attr>')
def deleteAttribute(attr):
	session.query(Attribute).filter_by(id=attr).delete()
	session.commit()
	return redirect(url_for('attributes'))

@app.route('/creatures/new')
def newCreature():
	return render_template('Creatures/form.html')

@app.route('/creatures/create', methods=['POST'])
def createCreature():
	crea = Creature()
	crea.name = format(request.form['name'])
	crea.size = format(request.form['size'])
	crea.notes = format(request.form['notes'])
	try:
		session.add(crea)
		session.commit()
		if cr.notes:
			tts = gTTS(text=crea.notes, lang='en')
			tts.save('static/sounds/'+crea.name+'.mp3')
		return redirect(url_for('creatures'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Creatures/form.html', error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])


@app.route('/creatures/edit/<crea>')
def editCreature(crea):
	cr = session.query(Creature).filter_by(id=crea).one()
	dmgs = session.query(DamageType).all()
	at = session.query(Attribute).all()
	return render_template('Creatures/form.html', cr=cr, types=dmgs, attrs=at)

@app.route('/creatures/update/<crea>', methods=['POST'])
def updateCreature(crea):
	cr = session.query(Creature).filter_by(id=crea).one()
	cr.name = format(request.form['name'])
	cr.size = format(request.form['size'])
	cr.notes = format(request.form['notes'])
	lista = []
	for ra in request.form.getlist('resistances'):
		lista.append(session.query(DamageType).with_for_update(nowait=False, of=DamageType).filter_by(id=format(ra)).one())
	cr.resistances=lista
	lista = []
	for ra in request.form.getlist('immunities'):
		lista.append(session.query(DamageType).with_for_update(nowait=False, of=DamageType).filter_by(id=format(ra)).one())
	cr.immunities=lista
	lista = []
	for ra in request.form.getlist('vulnerabilities'):
		lista.append(session.query(DamageType).with_for_update(nowait=False, of=DamageType).filter_by(id=format(ra)).one())
	cr.vulnerabilities=lista
	lista = []
	for ra in request.form.getlist('dmgTypes'):
		lista.append(session.query(DamageType).with_for_update(nowait=False, of=DamageType).filter_by(id=format(ra)).one())
	cr.dmgTypes=lista
	lista = []
	for ra in request.form.getlist('attributes'):
		lista.append(session.query(Attribute).with_for_update(nowait=False, of=Attribute).filter_by(id=format(ra)).one())
	cr.attributes=lista
	
	try:
		session.commit()
		if cr.notes:
			tts = gTTS(text=cr.notes, lang='en')
			tts.save('static/sounds/'+cr.name+'.mp3')
		return redirect(url_for('creatures'))
	except exc.IntegrityError:
		session.rollback()
		dmgs = session.query(DamageType).all()
		at = session.query(Attribute).all()
		return render_template('Creatures/form.html', cr=cr, types=dmgs, attrs=at, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@app.route('/creatures/delete/<crea>')
def deleteCreature(crea):
	session.query(Creature).filter_by(id=crea).delete()
	session.commit()
	return redirect(url_for('creatures'))

@app.route('/creatures/<crea>/delete/<enc>')
def deleteEncounter(crea, enc):
	session.query(Encounter).filter_by(id=enc).delete()
	session.commit()
	return redirect(url_for('showCreature', crea=crea))

@app.route('/creatures/<crea>/new')
def newEncounter(crea):
	return render_template('Encounters/form.html', cr=crea)

@app.route('/creatures/<crea>/create/', methods=['POST'])
def createEncounter(crea):
	enc = Encounter()
	enc.hitsLand = format(request.form['hitsLand'])
	enc.atksLand = format(request.form['atksLand'])
	enc.dmgLand = format(request.form['dmgLand'])
	enc.atkBonus = format(request.form['atkBonus'])
	enc.hitsRec = format(request.form['hitsRec'])
	enc.atksRec = format(request.form['atksRec'])
	enc.ac = format(request.form['ac'])
	enc.dmgRec = format(request.form['dmgRec'])
	enc.creature_id = crea
	try:
		session.add(enc)
		session.commit()
		return redirect(url_for('showCreature', crea=crea))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Encounters/form.html', cr=crea, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@app.route('/creatures/<crea>/edit/<enc>')
def editEncounter(crea,enc):
	en = session.query(Encounter).filter_by(id=enc).one()
	return render_template('Encounters/form.html', cr=crea, en=en)

@app.route('/creatures/<crea>/update/<enc>', methods=['POST'])
def updateEncounter(crea, enc):
	en = session.query(Encounter).filter_by(id=enc).one()
	en.hitsLand = format(request.form['hitsLand'])
	en.atksLand = format(request.form['atksLand'])
	en.dmgLand = format(request.form['dmgLand'])
	en.atkBonus = format(request.form['atkBonus'])
	en.hitsRec = format(request.form['hitsRec'])
	en.atksRec = format(request.form['atksRec'])
	en.ac = format(request.form['ac'])
	en.dmgRec = format(request.form['dmgRec'])
	try:
		session.commit()
		return redirect(url_for('showCreature', crea=crea))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Encounters/form.html', cr=crea, en=en, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0',port=5000)