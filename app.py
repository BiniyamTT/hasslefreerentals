import os
import datetime
import json

from cs50 import SQL
from flask import Flask, flash, jsonify,redirect, render_template, request, session
from flask_session import Session
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Initialize Flask-Breadcrumbs
Breadcrumbs(app=app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///rentals.db")

# Create users table
db.execute  ("""
                CREATE TABLE IF NOT EXISTS users
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    username TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phonenumber TEXT NOT NULL,
                    usertype TEXT NOT NULL
                )
            """)

# Create equipments table
db.execute  ("""
                CREATE TABLE IF NOT EXISTS equipments(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    owner_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    sub_category TEXT NOT NULL,
                    brand TEXT NOT NULL,
                    model TEXT NOT NULL,
                    license_plate_no INTEGER NOT NULL,
                    fuel_type TEXT NOT NULL,
                    hp INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    hourly_rate TEXT NOT NULL,
                    advance TEXT NOT NULL,
                    duration TEXT NOT NULL,
                    location TEXT NOT NULL,
                    FOREIGN KEY (owner_id) REFERENCES users(user_id)
                )
            """)




# Configure global usertypes
USER_TYPES = ["Lessor", "Lessee"]

# Configure global equipment categories
CAT =   {
            "Asphalt": ["Asphalt Layer", "Asphalt Scrapper"],
            "Compaction": ["Single Drum Smooth Wheeled Roller","Double Drum Smooth Wheeled Roller", "Padfoot Roller", "Pneumatic Roller"],
            "Concrete and Masonry": ["Concrete Pump Truck", "Concrete Mixer Truck",],
            "Earthwork":["Excavator", "Mini-Excavator", "Bull-Dozer", "Grader", "Loader", "Back Hoe"],
            "Trucks and Trailers":["Flat Bed Trucks", "Dump Trucks", "Low-bed Trucks"]
         }


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Home page > index.html> /
@app.route("/")
@register_breadcrumb(app, '.', 'Home')
def index():
       return render_template("index.html", CAT = CAT)


# Register Users to Webapp
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
    
        # Ensure username was submitted
        if not request.form.get("username"):
                return apology("must provide username", 403)
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username is not already taken
        if len(rows) == 1:
            return apology("username already taken", 403)
        
        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation") :
            return apology("must provide password", 403)
        
        # Ensure password matches with confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords dont match", 403)
        
        # Register username and password hash into db
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))
        email = request.form.get("email")
        phonenumber = request.form.get("phonenumber")
        usertype = request.form.get("usertype")
        
        db.execute("INSERT INTO users(username, hash, email, phonenumber, usertype) VALUES(?, ?, ?, ?, ?)", username, hash, email, phonenumber, usertype)

        # Redirect to login page
        flash("You were successfully registered, log in to continue")
        return render_template("login.html")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html", usertypes = USER_TYPES)

# Log Users in
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["usertype"] = rows[0]["usertype"]
        
        print("--------------------------------------------------")
        print(session["user_id"])
        print(session["usertype"])
        
        
        # Redirect user to home page
        flash("Successfully logged in")
        return render_template("index.html", CAT = CAT, usertype = session["usertype"])
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Log users out
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Equipments page will let users browse equipments on database
@app.route("/equipments")
@login_required
def equipments():
    return render_template("equipments.html", CAT = CAT)


@app.route("/equipmentdetail", methods=["GET", "POST"])
@login_required
def equipmentdetail():
    if request.method == "GET":
        return render_template("equipmentdetail.html", CAT = CAT)
    else:
        return render_template("equipmentdetail.html", CAT = CAT)
        


@app.route("/screturn")
def screturn():
    cat = request.args.get("cat")
    if cat:
        subcat = CAT[cat]       
    else:
        subcat = []
    return jsonify(subcat)




@app.route("/eqregister", methods=["GET", "POST"])
@login_required
def eqregister():
    if request.method == "POST":
        CAT_SET = request.form.get("category")
        return redirect ("/eqregister")
    else:
        return render_template("eqregister.html", CAT = CAT)
    
 