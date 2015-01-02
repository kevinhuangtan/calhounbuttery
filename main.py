from gevent import monkey
monkey.patch_all()

from threading import Thread
from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.socketio import SocketIO

# Set up app with debugging
app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
thread = None


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['BUTTERY_DATABASE_URL']
db = SQLAlchemy(app)

# for flask-login -- secret key needed to use sessions
app.secret_key = os.environ['BUTTERY_SECRET_KEY']
