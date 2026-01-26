from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

# ---------------- LOGIN -----------------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        return redirect(url_for(role))
    return render_template("login.html")

# ---------------- FARMER -----------------
@app.route("/farmer", methods=["GET","POST"])
def farmer():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        crop_name = request.form["crop_name"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        cur.execute(
            "INSERT INTO crops (crop_name, quantity, price) VALUES (?, ?, ?)",
            (crop_name, quantity, price)
        )
        conn.commit()

    cur.execute("SELECT * FROM crops")
    crops = cur.fetchall()
    conn.close()

    return render_template("farmer.html", crops=crops)

# ---------------- BUYER -----------------
@app.route("/buyer")
def buyer():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM crops")
    crops = cur.fetchall()
    conn.close()

    return render_template("buyer.html", crops=crops)

# ---------------- ADMIN -----------------
@app.route("/admin")
def admin():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM crops")
    crops = cur.fetchall()
    conn.close()

    return render_template("admin.html", crops=crops)

# ---------------- DELETE -----------------
@app.route("/delete/<int:id>")
def delete_crop(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM crops WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)
