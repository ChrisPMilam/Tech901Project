from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")



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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if not rows:
            return apology("invalid username and/or password", 403)

        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/sqlist")
def index():
    """Show list of questions"""
    questions = db.execute("SELECT * FROM Question WHERE User_ID = :userid", userid=session["user_id"])

    return render_template("sQuestions.html", questions=questions)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was submitted
        elif not request.form.get("password_confirm"):
            return apology("must confirm password", 403)

        # Ensure password was submitted
        elif not (request.form.get("password_confirm") == request.form.get("password")):
            return apology("passwords do no match", 403)

        # generate password hash
        hash = generate_password_hash(request.form.get("password"))

        # Insert user into database for username
        rows = db.execute("INSERT INTO users (UserName, Password, Role) VALUES(:username, :hash, :role)",
                          username=request.form.get("username"), hash=hash, role="Student")

        if not rows:
            return apology("user already exists", 403)

        # Ensure username exists and password is correct
        #if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #    return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    return apology("TODO")


@app.route("/register_teacher", methods=["GET", "POST"])
def register_teacher():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was submitted
        elif not request.form.get("password_confirm"):
            return apology("must confirm password", 403)

        # Ensure password was submitted
        elif not (request.form.get("password_confirm") == request.form.get("password")):
            return apology("passwords do no match", 403)

        # generate password hash
        hash = generate_password_hash(request.form.get("password"))

        # Insert user into database for username
        rows = db.execute("INSERT INTO users (UserName, Password, Role) VALUES(:username, :hash, :role)",
                          username=request.form.get("username"), hash=hash, role="Teacher")

        if not rows:
            return apology("user already exists", 403)

        # Ensure username exists and password is correct
        #if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #    return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register_teacher.html")
    return apology("TODO")


@app.route("/question", methods=["GET", "POST"])
def question():

    # Get question
    if request.method == "GET":
        return render_template("studentform.html")
    if request.method == "POST":
        if not request.form.get("title"):
            return error ("Please provide a question title.")

        # Post form question to database
        db.execute("INSERT INTO project (title, description, code, id) VALUES(:title, :description, :code, :id)",
                    title = request.form.get("title"), description = request.form.get("description"), code = request.form.get("code"), id=session["user_id"])
        # Return to main forum
    return redirect(url_for("index"))


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
