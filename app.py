from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"


# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ================= PRODUCTS =================
products = [
    {"id":1,"name":"Brocolli - 1 Kg","price":120,"img":"brocolli.jpg"},
    {"id":2,"name":"Carrot - 1 Kg","price":60,"img":"carrot.jpg"},
    {"id":3,"name":"Tomato - 1 Kg","price":40,"img":"tomato.jpg"},
    {"id":4,"name":"Walnuts - 1/4 Kg","price":170,"img":"walnut.jpg"},
    {"id":5,"name":"Cashews - 1 Kg","price":650,"img":"cashew.jpg"},
    {"id":6,"name":"Beans - 1 Kg","price":70,"img":"beans.jpg"},
    {"id":7,"name":"Beetroot - 1 Kg","price":50,"img":"beetroot.jpg"},
    {"id":8,"name":"Brinjal - 1 Kg","price":55,"img":"brinjal.jpg"},
    {"id":9,"name":"Cucumber - 1 Kg","price":30,"img":"cucumber.jpg"},
    {"id":10,"name":"Cauliflower - 1 Kg","price":45,"img":"cauliflower.jpg"},
    {"id":11,"name":"Chilli - 1/4 Kg","price":15,"img":"chilli.jpg"}
]


# ================= COUNTRIES =================
countries = [
    "India","United States","United Kingdom","Canada","Australia",
    "Germany","France","Italy","Spain","Netherlands",
    "China","Japan","South Korea","Brazil","Mexico",
    "South Africa","Russia","UAE","Singapore","New Zealand"
]


# ================= HOME =================
@app.route('/')
def index():
    cart = session.get("cart", {})
    user = session.get("user")

    total_items = sum(cart.values())
    total_price = sum(
        p["price"] * cart.get(str(p["id"]), 0)
        for p in products
    )

    return render_template(
        "index.html",
        products=products,
        total_items=total_items,
        total_price=total_price,
        user=user,
        cart=cart
    )


# ================= ADD =================
@app.route('/add', methods=["POST"])
def add():
    pid = request.form["id"]

    cart = session.get("cart", {})
    cart[pid] = cart.get(pid, 0) + 1
    session["cart"] = cart

    return redirect(request.referrer or "/")


# ================= DECREASE =================
@app.route('/decrease', methods=["POST"])
def decrease():
    pid = request.form["id"]
    cart = session.get("cart", {})

    if pid in cart:
        cart[pid] -= 1
        if cart[pid] <= 0:
            del cart[pid]

    session["cart"] = cart
    return redirect(request.referrer or "/")


# ================= REMOVE =================
@app.route('/remove', methods=["POST"])
def remove():
    pid = request.form["id"]
    cart = session.get("cart", {})

    if pid in cart:
        del cart[pid]

    session["cart"] = cart
    return redirect(request.referrer or "/")


# ================= CLEAR CART =================
@app.route('/clear_cart', methods=["POST"])
def clear_cart():
    session.pop("cart", None)
    session.pop("discount", None)
    return redirect(request.referrer or "/")


# ================= PROMO =================
@app.route('/apply_promo', methods=["POST"])
def apply_promo():
    code = request.form["code"]

    if code == "SAVE25":
        session["discount"] = 0.25
    else:
        session["discount"] = 0

    return redirect("/cart")


# ================= CART =================
@app.route('/cart')
def cart():
    cart = session.get("cart", {})
    items = []
    total = 0

    for p in products:
        if str(p["id"]) in cart:
            qty = cart[str(p["id"])]
            subtotal = qty * p["price"]
            total += subtotal
            items.append({
                "p": p,
                "qty": qty,
                "subtotal": subtotal
            })

    discount = session.get("discount", 0)
    final_total = total - (total * discount)

    # FIX: remove discount if cart empty
    if total == 0:
        session.pop("discount", None)
        discount = 0
        final_total = 0

    return render_template(
        "cart.html",
        items=items,
        total=total,
        final_total=final_total,
        discount=discount
    )


# ================= CHECKOUT =================
@app.route('/checkout')
def checkout():
    return render_template("checkout.html", countries=countries)


@app.route('/place_order', methods=["POST"])
def place_order():
    if not request.form.get("agree"):
        return render_template("checkout.html", error="Please accept terms", countries=countries)

    session.pop("cart", None)
    session.pop("discount", None)
    return redirect("/success")


@app.route('/success')
def success():
    return render_template("success.html")


# ================= LOGIN =================
@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        cur = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            msg = "Invalid Username or Password"

    return render_template("login.html", msg=msg)


# ================= REGISTER =================
@app.route('/register', methods=["GET", "POST"])
def register():
    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        db.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username, password)
        )
        db.commit()

        msg = "Registered Successfully"

    return render_template("register.html", msg=msg)


# ================= FORGOT =================
@app.route('/forgot', methods=["GET", "POST"])
def forgot():
    msg = ""

    if request.method == "POST":
        username = request.form["username"]

        db = get_db()
        cur = db.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        if user:
            msg = "Password reset link sent (demo)"
        else:
            msg = "User not found"

    return render_template("forgot.html", msg=msg)


# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect("/")


# ================= RUN =================
if __name__ == "__main__":
     app.run(host="0.0.0.0", port=10000)