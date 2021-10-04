from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


@app.route('/movsrcresult', methods=["GET", "POST"])
def movsrcresult():
    return render_template('movie_det.html')


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


if __name__ == "__main__":
    app.run(debug=True)
