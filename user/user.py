# all the imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from main import app, db
from models import *
from kitchen.kitchen import *
from main import socketio
from flask.ext.socketio import SocketIO, emit

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/user', methods=['GET', 'POST'])
def user_page():
	if "logged_in" in session:
		user = User.query.filter_by(id=session['id']).first()
		return render_template('user_page.html', title='Home', name=user.name, bucks=user.buttery_bucks)
	return redirect('/')

@user.route('/submit_order', methods=['GET','POST'])
def handle_submit_order():
	order = request.form["order"]
	comments = request.form["comments"]
	print(order + comments)
	if (order !=""):
		user = User.query.filter_by(id=session['id']).first()
		bucks = 'cash';
		if (user.buttery_bucks > 0 and (float(user.buttery_bucks) > float(menu[order]))):
			user.buttery_bucks = float(float(user.buttery_bucks) - float(menu[order]));
			bucks = 'bucks'
		g.order = Order(order=order, comments=comments, delivered = False, parent_id=session['id'], bucks_payment = bucks)
		db.session.add(g.order)
		db.session.commit()
		session['has_order'] = True
		return redirect ('/user')
	return render_template('user_page.html', title='Home', name=session['name'])

@user.route('/logout', methods=['GET', 'POST'])
def logout():
	session.clear()
	return redirect('/')

@socketio.on('connect', namespace='/test')
def on_connect():
	#whenever a new connect, kitchen refreshes
	orders = Order.query.filter_by(delivered=False).all()
	recent_orders = Order.query.filter_by(delivered=True).all()
	emit('clear kitchen sheet', broadcast=True)
	emit('clear customer sheet', broadcast=True)
	print('hello')
	for order in orders:
		order_s = str(order.order)
		comments = str(order.comments)
		delivered = str(order.delivered)
		customer = str(User.query.filter_by(id=order.parent_id).first().name)
		emit('print orders customer',
		{'order': order_s, 'comments': comments,'delivered': delivered,'name': customer, 'id':order.id}, 
		broadcast=True)
		print(order_s)
		emit('print orders kitchen',
		{'order': order_s, 'comments': comments,'delivered': delivered,'name': customer, 'id':order.id, 'payment':order.bucks_payment}, 
		broadcast=True)
	recent_delivered = 0
	for recent_order in reversed(recent_orders):
		deliver_date= recent_order.deliver_date
		time_since=timesince(deliver_date)
		if (time_since < 120 and recent_delivered < 5):
			order_s = str(recent_order.order)
			comments = str(recent_order.comments)
			delivered = str(recent_order.delivered)
			customer = str(User.query.filter_by(id=recent_order.parent_id).first().name)
			recent_delivered = recent_delivered + 1
			emit('print recent orders customer',
			{'order': order_s, 'comments': comments,'delivered': delivered,'name': customer, 'id':recent_order.id}, 
			broadcast=True)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
	print('Client disconnected')

def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.now()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    # return minutes passed
    return diff.seconds/60

    # for period, singular, plural in periods:
        
    #     if period:
    #         return "%d %s ago" % (period, singular if period == 1 else plural)

    # return default


