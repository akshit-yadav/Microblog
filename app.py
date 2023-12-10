import os
import datetime
#import secrets as sc
from flask import (
    Flask,
    session,
    render_template,
    request,
    abort,
    flash,
    redirect,
    url_for
)
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://akshit:Mongodb158@microblog-application.rsupmis.mongodb.net/test")
app.db = client.Microblog

app.secret_key = "-duELRLaJ8k9X757Lt-foA"

entries = []
users = {}


@app.route("/")
def home():
    session.clear()
    return render_template("login.html", email = session.get("email"))


@app.route("/protected", methods=["GET", "POST"])
def protected():
    if not session.get("email"):
        abort(401)
    if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            entries.append((entry_content,formatted_date ))
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        
    entries_with_date = [
        (
            entry[0],
            entry[1],
            datetime.datetime.strptime(entry[1], "%Y-%m-%d").strftime("%b %d")
        )
        for entry in entries
    ]
    return render_template("home.html", entries=entries_with_date)  


@app.route("/login", methods=["GET", "POST"])
def login():
#   email = "akshit.crown@gmail.com"
#   password = "123456"

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if users.get(email) == password:
            session["email"] = email
            return redirect(url_for("protected"))
        else:
            flash("Incorrect Email or Password. ")
            flash("If you are a new user, please Sign up first.")
    return render_template("login.html")


@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        users[email] = password
        session["email"] = email
        flash("Successfully Signed Up.😄")
        return redirect(url_for("login"))


    return render_template("signup.html")

#@app.route("/dropsession")
#def dropsession():
#    session.pop("email", None)
#    return render_template('home.html')



