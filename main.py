from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("main.html")


@app.route('/login')
def login():
    return render_template("signin.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/logout')
def logout():
    return redirect(url_for("home"))
    # return render_template("logout.html")


@app.route('/validate', methods=["GET", "POST"])
def validate():
    return redirect(url_for("profile"))


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/movrec')
def movrec():
    return render_template('rec_search.html')


@app.route('/movrecresult', methods=["GET", "POST"])
def movrecresult():
    return render_template("rec_result.html")


@app.route('/movsrc')
def movsrc():
    return render_template('mov_search.html')


@app.route('/movsrcresult', methods=["GET", "POST"])
def movsrcresult():
    return render_template('movie_det.html')


@app.route('/topten')
def topten():
    return render_template("topten.html")


if __name__ == "__main__":
    app.run(debug=True)
