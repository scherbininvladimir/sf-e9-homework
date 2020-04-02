from app import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
metadata = Base.metadata

class Event(Base):
    __tablename__ = 'event_test'
    _id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, db.ForeignKey('user_test.login'))
    start_time = db.Column(db.DateTime, unique=False, nullable=False)
    end_time = db.Column(db.DateTime, unique=False, nullable=False)
    title = db.Column(db.String(256), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)

class User(Base):
    __tablename__ = 'user_test'
    login = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.login

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active