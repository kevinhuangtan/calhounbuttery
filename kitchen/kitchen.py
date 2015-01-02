from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from main import app, db
from user.models import *
from main import socketio
from flask.ext.socketio import SocketIO, emit
from datetime import datetime

kitchen = Blueprint('kitchen', __name__, template_folder='templates')

@kitchen.route('/kitchen', methods=['GET', 'POST'])
def kitchen_socket():
	if 'chef_logged_in' in session:
		orders = Order.query.filter_by(delivered=False).all()
		if request.method == 'POST':
			order_id = request.form['id']
			order = Order.query.get(order_id) 
			order.delivered = True
			order.deliver_date=datetime.now()
			db.session.commit()
			# finish post request
			return redirect('/kitchen')
		return render_template('kitchen_page_socket.html', title='Kitchen', orders=orders)
	return redirect('/kitchen_login')

@kitchen.route('/kitchen_login', methods=['GET','POST'])
def kitchen_login_handler():
	if request.method == 'POST':
		password = request.form['password']
		if password == "dopeasskitchen":
			session['chef_logged_in'] = True; 
			return redirect('/kitchen')
		print ('wrong password')
	return render_template('kitchen_login.html')

@kitchen.route('/kitchen_logout', methods=['GET', 'POST'])
def kitchen_logout():
	session.clear()
	return redirect('/index')

@kitchen.route('/submit_bucks', methods=['GET', 'POST'])
def handle_bucks():
	users = User.query.all()
	if User.query.filter_by(name=request.form['name']).count() > 0:
		user = User.query.filter_by(name=request.form['name']).first()
		user.buttery_bucks = float(user.buttery_bucks) + float(request.form['bucks'])
		db.session.commit()
		return redirect('/kitchen')
	return redirect('/kitchen')





