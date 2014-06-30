import model
import csv
import datetime

def load_users(session):
    # use u.user
    with open('seed_data/u.user', 'rb') as f:
        reader = csv.reader(f, delimiter = '|')
        for row in reader: # user id | age | gender | occupation | zip code
            x = model.User()
            x.id = int(row[0]) # user id
            x.age = int(row[1]) # age
            x.zipcode = row[4] #zipcode
            session.add(x)
        session.commit()

def convert_to_datetime(str_date):
    # '01-Feb-1998'
    if str_date != '':
        new_datetime = datetime.datetime.strptime(str_date, "%d-%b-%Y")
        return new_datetime

def load_movies(session):
    # use u.item
    with open('seed_data/u.item','rb') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader: # [user id,item id,rating,timestamp]
            x = model.Movie()
            x.id = int(row[0]) # movie id
            x.name = str(row[1]) # movie title
            x.released_at = convert_to_datetime(row[2]) #release date
            x.imdb_url = str(row[4]) #IMDb URL
            session.add(x)
        session.commit()

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data','rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader: # [user id,item id,rating,timestamp]
            x = model.Rating()
            x.user_id = int(row[0])
            x.movie_id = int(row[1])
            x.rating = int(row[2])
            session.add(x)
        session.commit()

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    # load_ratings(session)
    # load_movies(session)
    load_users(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
