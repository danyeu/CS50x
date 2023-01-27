import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    owned = db.execute("SELECT * FROM owned WHERE id = ?", session["user_id"])
    stocks = []
    total = 0
    for stock in owned:
        data = lookup(stock["symbol"])
        owned_value = data["price"] * stock["shares"]
        total += owned_value
        tempdict = {"symbol": stock["symbol"], "company_name": data["name"], "shares_owned": stock["shares"], "price": usd(data["price"]), "value_owned": usd(owned_value)}
        stocks.append(tempdict)

    total += cash

    cash = usd(cash)
    total = usd(total)

    return render_template("portfolio.html", stocks = stocks, cash = cash, total = total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)

        # check if valid symbol
        now = datetime.now()
        data = lookup(request.form.get("symbol").strip())
        if data is None:
            return apology("invalid symbol", 400)

        shares = request.form.get("shares")
        # check if shares is a non-negative integer
        if not shares.isdigit():
            return apology("shares must be a positive integer", 400)
        # check if shares > 0
        try:
            shares = int(shares)
            if shares <= 0:
                raise Exception("non-positive number")
        except:
            return apology("shares must be a positive integer", 400)

        # check if enough cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        cost = shares * data["price"]
        if cash < cost:
            return apology("not enough cash", 400)

        # buy
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - cost, session["user_id"])
        rows = db.execute("SELECT * FROM owned WHERE id = ? AND symbol = ?", session["user_id"], data["symbol"])
        if len(rows) == 0:
            db.execute("INSERT INTO owned (id, symbol, shares) VALUES(?,?,?)", session["user_id"], data["symbol"], shares)
        else:
            existing_shares = db.execute("SELECT shares FROM owned WHERE id = ? AND symbol = ?", session["user_id"], data["symbol"])[0]["shares"]
            new_shares = existing_shares + shares
            db.execute("UPDATE owned SET shares = ? WHERE id = ? AND symbol = ?", new_shares, session["user_id"], data["symbol"])

        # history
        db.execute("INSERT INTO history (id, symbol, shares, price, instruction, date) VALUES(?,?,?,?,?,?)", session["user_id"], data["symbol"], shares, data["price"], "Buy", now)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE id = ?", session["user_id"])
    transactions = []
    for transaction in history:
        tempdict = {"instruction": transaction["instruction"], "symbol": transaction["symbol"], "shares_transacted": transaction["shares"], "price": usd(transaction["price"]), "date": transaction["date"]}
        transactions.append(tempdict)

    return render_template("history.html", transactions = transactions)


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

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Change user password"""
    if request.method == "POST":
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation password", 403)
        # Ensure passwords match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 403)

        # Update database
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("password")), session["user_id"])

        # Logout and redirect
        session.clear()
        return redirect("/")
    else:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        return render_template("changepassword.html", username = username)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        data = lookup(request.form.get("symbol").strip())
        if data is None:
            return apology("invalid symbol", 400)
        else:
            return render_template("quoted.html", company_name = data["name"], symbol = data["symbol"], price = usd(data["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation password", 400)
        # Ensure passwords match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("username already taken", 400)

        # Add to database
        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    owned = db.execute("SELECT symbol FROM owned WHERE id = ?", session["user_id"])
    symbols = []
    for row in owned:
        symbols.append(row["symbol"])

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)

        # check if valid symbol
        if request.form.get("symbol") not in symbols:
            return apology("invalid symbol", 400)

        shares = request.form.get("shares")
        # check if shares is a non-negative integer
        if not shares.isdigit():
            return apology("shares must be a positive integer", 400)
        # check if shares > 0
        try:
            shares = int(shares)
            if shares <= 0:
                raise Exception("non-positive number")
        except:
            return apology("shares must be a positive integer", 400)

        # check if enough shares
        shares_owned = db.execute("SELECT shares FROM owned WHERE id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))[0]["shares"]
        if shares_owned < shares:
            return apology("not enough shares", 400)

        # sell
        now = datetime.now()
        data = lookup(request.form.get("symbol"))
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        # cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + shares * data["price"], session["user_id"])
        # owned
        if shares_owned - shares == 0:
            db.execute("DELETE FROM owned WHERE id = ? AND symbol = ?", session["user_id"], data["symbol"])
        else:
            db.execute("UPDATE owned SET shares = ? WHERE id = ? AND symbol = ?", shares_owned - shares, session["user_id"], data["symbol"])
        # history
        db.execute("INSERT INTO history (id, symbol, shares, price, instruction, date) VALUES(?,?,?,?,?,?)", session["user_id"], data["symbol"], shares, data["price"], "Sell", now)

        return redirect("/")
    else:
        return render_template("sell.html", symbols = symbols)
