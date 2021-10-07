from pprint import pprint
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

TMDB_API_KEY = '7a6f6a890df3e553f8aaf75ec5cf078e'
RAPIDAPI_KEY = 'cf61825fe6mshaa7ecf5fa25b75bp1c5a42jsn373bd69cfeb3'


class User(db.Model):
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    eml = db.Column(db.String(100), nullable=False)
    pswd = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(100), nullable=False)
    dbrth = db.Column(db.String(100), nullable=False)
    fvdir = db.Column(db.String(100), nullable=False)
    fvmov = db.Column(db.String(100), nullable=False)
    prflng = db.Column(db.String(100), nullable=False)
    prfgen = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


db.create_all()


# *----- Main Landing Page -----*
@app.route('/')
def home():
    return render_template("main.html")


# *----- Main Landing Page -----*

# *----- Signup & Profile Creation -----*

@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/profcrt', methods=["GET", "POST"])
def profcrt():
    if request.method == "POST":
        usnm = request.form.get('name')
        eml = request.form.get('email')
        pswd = request.form.get('pwd')
        dbr = request.form.get('db')
        dob = datetime.strptime(dbr, "%Y-%m-%d")
        dobst = dob.strftime("%d %b, %Y")
        bio = request.form.get('bio')
        favdir = request.form.get('favdir')
        favmov = request.form.get('favmov')
        preflang = request.form.get('preflang')
        prefgen = request.form.get('prefgen')
        print(usnm, eml, pswd, dobst, bio, favdir, favmov, preflang, prefgen)
        new_user = User(
            username=usnm,
            eml=eml,
            pswd=pswd,
            bio=bio,
            dbrth=dobst,
            fvdir=favdir,
            fvmov=favmov,
            prflng=preflang,
            prfgen=prefgen
        )
        already_exists = db.session.query(User.username).filter_by(username=usnm).first() is not None
        if already_exists:
            data = ['Uh Oh!!', "This username already exists.", 'Signup Screen', 'signup']
            return render_template("intermd.html", data=data)
        else:
            db.session.add(new_user)
            db.session.commit()
            data = ['Success!!', "Your accounht has been created successfully!!", 'Profile', 'profile']
            return render_template("intermd.html", data=data)


# *----- Signup & Profile Creation -----*


# *----- Login and validation -----*

@app.route('/login')
def login():
    return render_template("signin.html")


@app.route('/validate', methods=["GET", "POST"])
def validate():
    if request.method == "GET":
        return redirect(url_for("profile"))
    if request.method == "POST":
        usnm = request.form.get('name')
        pswd = request.form.get('pwd')
        exists = db.session.query(User.username).filter_by(username=usnm).first() is not None
        if exists:
            user_to_verify = User.query.get(usnm)
            if (usnm == user_to_verify.username) and (pswd == user_to_verify.pswd):
                data = ['Success!!', "You have been logged in successfully!!", 'Continue', 'profile']
                return render_template("intermd.html", data=data)
            else:
                data = ['Oops!!', "Your Username and Password Do Not Match", 'Login Screen', 'login']
                return render_template("intermd.html", data=data)
        else:
            data = ['Oops!!', "This Username Does Not Exist", 'Signup Screen', "signup"]
            return render_template("intermd.html", data=data)


# *----- Login and validation -----*

# *----- Logout Path -----*

@app.route('/logout')
def logout():
    data = ['GoodBye', "Thank you for visiting our site", 'Logout', 'home']
    return render_template("intermd.html", data=data)


# *----- Logout Path -----*

# *----- Profile Path -----*

@app.route('/profile')
def profile():
    return render_template('profile.html')


# *----- Profile Path -----*

# *----- Movie Detail Search Path -----*

@app.route('/movsrc')
def movsrc():
    return render_template('mov_search.html')


def get_movies(movname):
    # Getting the Movie ID from the Movie name
    movie_id_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movname}"
    image_url = "http://image.tmdb.org/t/p/w500"
    movies = requests.get(f"{movie_id_url}").json()['results'][:5]
    # pprint(movies)
    movie_data = []
    index = 97
    for movie in movies:
        new_movie = {
            'id': movie['id'],
            'css': chr(index),
            'title': movie['title'],
            'backdrop': f"{image_url}{movie['backdrop_path']}",
            'poster': f"{image_url}{movie['poster_path']}",
            'year': movie['release_date'].split('-')[0]
        }
        movie_data.append(new_movie)
        index += 1
    # pprint(movie_data)
    return movie_data


@app.route('/movsrcresall', methods=["GET", "POST"])
def movsrcresall():
    movname = request.form.get('movname')
    movies = get_movies(movname)
    return render_template('allmovres.html', movies=movies)


def get_movie_deets(movie_id):
    # All required API queries
    image_url = "http://image.tmdb.org/t/p/w500"
    cast_info_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?"
    movie_data_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    mov_dat_params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    # Getting Cast Info and Director
    director = ""
    cast_data = []
    response = requests.get(cast_info_url, params=mov_dat_params).json()
    cast = response['cast'][:6]
    crew = response['crew']
    for i in crew:
        if i['job'] == "Director":
            director = i['name']
            break
    for i in cast:
        tmp = {
            'actor': i['original_name'],
            'character': i['character'],
            'img': f"{image_url}{i['profile_path']}"
        }
        cast_data.append(tmp)

    # Getting Movie Info
    response = requests.get(movie_data_url, params=mov_dat_params).json()
    # pprint(response)
    genres = []
    for i in response['genres']:
        genres.append(i['name'])
    languages = []
    for i in response['spoken_languages']:
        languages.append(i['english_name'])
    movie_data = {
        'title': response['original_title'],
        'overview': response['overview'],
        'tag': response['tagline'],
        'runtime': response['runtime'],
        'rating': response['vote_average'],
        'year': response['release_date'].split('-')[0],
        'genres': genres,
        'language': languages,
        'poster': f"{image_url}{response['poster_path']}",
        'backdrop': f"{image_url}{response['backdrop_path']}",
        'director': director
    }
    # pprint(cast_data)
    # pprint(movie_data)
    all_data = [cast_data, movie_data]
    return all_data


@app.route('/movsrcresult/<int:movid>', methods=["GET", "POST"])
def movsrcresult(movid):
    data = get_movie_deets(movid)
    return render_template('movie_det.html', data=data)


# *----- Movie Detail Search Path -----*

# *----- Movie Recommendation Search Path -----*

@app.route('/movrec')
def movrec():
    return render_template('rec_search.html')


@app.route('/movrecresult', methods=["GET", "POST"])
def movrecresult():
    return render_template("rec_result.html")


# *----- Movie Recommendation Search Path -----*

# *----- Top Ten Path -----*

@app.route('/topten')
def topten():
    return render_template("topten.html")


# *----- Top Ten Path -----*

# *----- Testing Out Routes -----*

# *----- Testing Out Routes -----*

# *----- Running the Application on the Flask Server -----*

if __name__ == "__main__":
    app.run(debug=True)

# *----- Running the Application on the Flask Server -----*


# *----- Testing Out Functions -----*


# *----- Testing Out Stuff -----*
