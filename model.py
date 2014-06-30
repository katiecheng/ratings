from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime #SQL alchemy datatypes

from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None



Base = declarative_base()

### Class declarations go here

class User(Base): #base is how we declare a SQLAlchemy class
    __tablename__ = "users" # instances of class will be stored in SQL table "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

class Movie(Base): #base is how we declare a SQLAlchemy class
    __tablename__ = "movies" # instances of class will be stored in SQL table "users"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=True)
    released_at = Column(DateTime, nullable=True)
    imdb_url = Column(String(64), nullable=True)

class Rating(Base): #base is how we declare a SQLAlchemy class
    __tablename__ = "ratings" # instances of class will be stored in SQL table "users"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)

### End class declarations

def make_tables():
    global ENGINE
    Base.metadata.create_all(ENGINE)

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session() # instantiating a session to interact with the DB

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
