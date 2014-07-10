from flask import Flask, render_template, redirect, request
from flask import session as session
import model

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'


@app.route("/")
def show_home():
    return render_template("home.html")

# def index():
#     user_list = model.session.query(model.User).limit(5).all()
#     return render_template("user_list.html", users=user_list)

@app.route("/login", methods = ["GET"])
def show_login():
    return render_template("login.html")

@app.route("/login", methods = ["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    session["username"] = username
    session["password"] = password

    print session
    
    return redirect("/")


if __name__=="__main__":
    app.run()