import os
from sqlalchemy import Column, String, Integer, create_engine, ARRAY, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import json

from config import settings

database_name = settings.POSTGRES_DB
database_path = settings.DATABASE_URI
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

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
drop_and_init_db()
This will delete all entries and will create new ones.
'''
def drop_and_init_db(app):
    with app.app_context():
      db.drop_all()
      db.create_all()

      first_entry = Movie(
        title="Rainy Temple",
        release_date="2023-01-25 15:20:00",
      )
      first_entry.insert()

      second_entry = Movie(
        title="Messi's Way",
        release_date="2023-01-25 15:20:00",
      )
      second_entry.insert()

      third_entry = Movie(
        title="Most Wanted",
        release_date="2023-01-25 15:20:00",
      )
      third_entry.insert()

      first_actor = Actor(
          name='Arturo Valdes', 
          age=26, 
          gender='Male'
          )
      first_actor.insert()

      second_actor = Actor(
          name='Viki Jones', 
          age=34, 
          gender='Female'
          )
      second_actor.insert()

      third_actor = Actor(
          name='Goran Snipe', 
          age=12, 
          gender='Male'
          )
      third_actor.insert()

      first_performance = Performance.insert().values(
          actor_id=3, 
          movie_id=1
          )
      
      second_performance = Performance.insert().values(
          actor_id=2, 
          movie_id=2
          )
      db.session.execute(first_performance)
      db.session.execute(second_performance)
      db.session.commit()


'''
Performance

This table associates the Movie model and the Actor model.
'''

Performance = db.Table('performance',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id', ondelete='CASCADE'), nullable=False),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), nullable=False)
)   

'''
Actors
'''
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

'''
Movies
'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String, nullable = False)
  release_date = Column(DateTime, default=datetime.now(), nullable=False)
  actor = db.relationship('Actor', secondary=Performance, lazy='select', backref=db.backref('movies', lazy=True))

  def __init__(self, title, release_date):
    self.title = title
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
      'release_date': self.release_date
    }
