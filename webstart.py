"""
URL routing & initialization for webapp
"""
from os.path import join
import os
from main import app, socketio
from flask import send_from_directory, Blueprint, send_file
from flask import Flask, render_template

print "Starting webapp!"

from home.home import home
app.register_blueprint(home)

from user.user import user
app.register_blueprint(user)

from kitchen.kitchen import kitchen
app.register_blueprint(kitchen)

from analytics.analytics import analytics
app.register_blueprint(analytics)

if __name__ == '__main__':
	socketio.run(app, port=80)
