from main import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, unique=True) 
    name = db.Column(db.String(151))
    email = db.Column(db.String(152), unique=True) 
    password = db.Column(db.String(153)) 
    buttery_worker = db.Column(db.Boolean)
    buttery_bucks = db.Column(db.Float)
    phone_number = db.Column(db.Integer)
    user_date = db.Column(db.DateTime)

    __tablename__ = 'parent'
    order_history = relationship("Order")
    #tells Python how to print objects of class Usera

    def __repr__(self):
        return '<User %r>' % (self.name)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def get_id(self):
        return unicode(self.id)  # python 2

class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    order = db.Column(db.String(50))
    comments = db.Column(db.String(200))
    date = db.Column(db.DateTime)
    delivered = db.Column(db.Boolean())
    deliver_date = db.Column(db.DateTime)
    bucks_payment = db.Column(db.String(50))

    __tablename__ = 'child'
    parent_id = Column(Integer, ForeignKey('parent.id'))
    # customer_name = db.Column(db.Integer, db.ForeignKey('parent.name'))
    def __repr__(self):
        return '<User %r>' % (self.order)

    def get_id(self):
        return unicode(self.id)  # python 2

menu = dict([('mozz sticks', 1.25), ('buff chick wrap', 2.0), ('nutelladilla', 1.0),('cheese case', 1.0),('chicken case', 1.50),('burger', 2.0),('crack', .75),('chicken tender', 2)])

