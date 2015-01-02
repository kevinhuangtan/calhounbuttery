from gevent import monkey
monkey.patch_all()

from threading import Thread
from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.socketio import SocketIO

#ignore (allow you to print)
import logging
from logging import StreamHandler
file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
app.logger.addHandler(file_handler)

# Set up app with debugging
app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
thread = None

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    
app.logger.debug(SQLALCHEMY_DATABASE_URI)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

# for flask-login -- secret key needed to use sessions
app.secret_key = os.environ['BUTTERY_SECRET_KEY']
