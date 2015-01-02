from main import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey
from datetime import datetime

Base = declarative_base()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True) 
    password = db.Column(db.String(64)) 
    buttery_worker = db.Column(db.Boolean)
    buttery_bucks = db.Column(db.Float)
    phone_number = db.Column(db.Integer)
    user_date = db.Column(db.DateTime)

    __tablename__ = 'parent'
    order_history = relationship("Order")
    #tells Python how to print objects of class Usera

    def __repr__(self):
        return '<User %r>' % (self.name)

    def get_id(self):
        return unicode(self.id)  # python 2

class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    order = db.Column(db.String(50))
    comments = db.Column(db.String(200))
    date = db.Column(db.DateTime)
    delivered = db.Column(db.Boolean())
    deliver_date = db.Column(db.DateTime)

    __tablename__ = 'child'
    parent_id = Column(Integer, ForeignKey('parent.id'))
    customer_name = db.Column(db.Integer, db.ForeignKey('parent.name'))
    def __repr__(self):
        return '<User %r>' % (self.order)

    def get_id(self):
        return unicode(self.id)  # python 2

menu = dict([('mozz sticks', 1.50), ('buff chick wrap', 2), ('nutelladilla', 1),('cheese case', 1),('chicken case', 1.50),('burger', 2),('crack', .75),('chicken tender', 1)])

