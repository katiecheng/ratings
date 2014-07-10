from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime #SQL alchemy datatypes

from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

import correlation


engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here

class User(Base): #base is how we declare a SQLAlchemy class
    __tablename__ = "users" # instances of class will be stored in SQL table "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

    def similarity(self, other):
        u_ratings = {} # empty dict
        paired_ratings = [] # empty list
        for r in self.ratings: # for each rating in user1's ratings
            u_ratings[r.movie_id] = r # append {movie-id:rating-object} to dict

        for o_r in other.ratings: # for each rating in user2's ratings
            u_r = u_ratings.get(o_r.movie_id) # query, set u_r to rating if user1 has rated that movie
            if u_r: # if u_r has a value
                paired_ratings.append( (u_r.rating, o_r.rating) ) # append a tuple of user1 and user2's ratings

        if paired_ratings: # if user1 and user2 have both rated at least one movie in common
            return correlation.pearson(paired_ratings) # return their similarity coefficient
        else:
            return 0.0

    def predict_rating(self, movie):
        """fn made obsolete by predict_rating_weighted()"""
        ratings = self.ratings # first query happens here
        other_ratings = movie.ratings # second query happens here
        other_users = [ r.user for r in other_ratings ]
        similarities = [ (self.similarity(other_user), other_user) \
            for other_user in other_users ] # a bunch more query happens in similarity()
        similarities.sort(reverse = True)
        top_user = similarities[0]
        matched_rating = None
        for rating in other_ratings:
            if rating.user_id == top_user[1].id:
                matched_rating = rating
                break
        return matched_rating.rating * top_user[0]

    def predict_rating_weighted(self, movie):
        ratings = self.ratings # first query happens here
        other_ratings = movie.ratings # second query happens here
        similarities = [ (self.similarity(other_r.user), other_r.rating) \
            for other_r in other_ratings ] # a bunch more query happens in similarity()
        similarities.sort(reverse = True) # maybe irrelevant now
        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities: # if similarities is empty, return None
            return None
        numerator = sum([ r * similarity for similarity, r in similarities ])
        denominator = sum([ similarity[0] for similarity in similarities ])
        return numerator/denominator

class Movie(Base): #base is how we declare a SQLAlchemy class
    __tablename__ = "movies" # instances of class will be stored in SQL table "users"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=True)
    released_at = Column(DateTime, nullable=True)
    imdb_url = Column(String(64), nullable=True)

class Rating(Base): #base is how we declare a SQLAlchemy class
    __tablename__ = "ratings" # instances of class will be stored in SQL table "users"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    # ForeignKey references another column in another table 'table.column_name'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)

    user = relationship("User", backref = backref("ratings", order_by=id))
    # value of the attribute 'user' is a user object
    # on a user object, add an attribute named 'ratings' which is a list
    # 'ratings' is a list of ratings associated with that user
    movie = relationship("Movie", backref = backref("ratings", order_by=id))

### End class declarations

def make_tables():
    global ENGINE
    Base.metadata.create_all(ENGINE)

# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///ratings.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session() # instantiating a session to interact with the DB

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
