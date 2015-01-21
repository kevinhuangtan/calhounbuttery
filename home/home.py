from flask import Flask, request, session, g, redirect, render_template, flash, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from main import app, db
from user.models import *
from datetime import datetime

home = Blueprint('home', __name__, template_folder='templates')

@home.route('/', methods=['GET', 'POST'])
def index():
	if "logged_in" in session:
		return redirect('/user')
	return render_template('home.html')

#Action - Where should form data be sent on clicking submit. It's an url.
@home.route('/login', methods=['GET','POST'])
def handle_login():
	print(request.form['email'])
	print(request.form['password'])
	email = request.form['email']
	password = request.form['password']
	user = User.query.filter_by(email=email).first()
	if user != None:
		if user.verify_password(password):
			print('correct password')
			session['logged_in'] = True; 
			session['name'] = user.name
			session['id'] = user.id
			print(session['name'])
			return redirect('/user')
		else:
			print ('wrong password')
			return render_template('home.html', error="wrong password")
	return render_template('home.html', error="wrong username or password")

@home.route('/signup', methods=['GET','POST'])
def handle_signup():
	name = request.form['name']
	email = request.form['email']
	password = request.form['password']
	#all inputs are there
	check_if_exists = User.query.filter_by(email=email).first()
	if (check_if_exists):
		return render_template('home.html', error="email already exists")
	if ("@" not in email):
		print ('not valid email')
		return render_template('home.html', error="not valid email")
	if (name!="" and email!="" and password!=""):
		g.user = User(name=name, email=email, buttery_bucks=0, user_date =datetime.now())
		g.user.hash_password(password)
		db.session.add(g.user)
		db.session.commit()
		session['logged_in'] = True; 
		session['name'] = g.user.name
		session['id'] = g.user.id
		print(User.query.all())
		return redirect('/user')
	return render_template('home.html', error="field left blank")





