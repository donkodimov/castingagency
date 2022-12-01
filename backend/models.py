import os
from sqlalchemy import Column, String, Integer, create_engine, ARRAY, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

from config import settings

database_name = "castingagency"
database_path = settings.DATABASE_URI

db = SQLAlchemy()
migrate = Migrate()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
    db.app = app
    db.init_app(app)
    #db.create_all()
    migrate.init_app(app, db)
    

'''
Movies
'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String, nullable = False)
  genre = Column(ARRAY(String), nullable = False)
  rating = Column(Integer, nullable = False, default="0")
  release_date = Column(DateTime, nullable = False)

  def __init__(self, title, genre, release_date, rating):
    self.title = title
    self.genre = genre
    self.rating = rating
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'genre': self.genre,
      'rating': self.rating,
      'release_date': self.release_date
    }

class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    age = Column(Integer, nullable = False)
    gender = Column(String, nullable = False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
        }
    