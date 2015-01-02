from flask import Flask, request, session, g, redirect, render_template, flash, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from main import app, db
from user.models import *
from datetime import datetime

analytics = Blueprint('analytics', __name__, template_folder='templates')

@analytics.route('/analytics', methods=['GET', 'POST'])
def analytics_route():
	history = dict()
	for i in menu:
		history[i] = Order.query.filter_by(order=i).count()
	print (history)
	return render_template('analytics.html', history = history, menu=menu)




