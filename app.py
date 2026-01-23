from flask import Flask, render_template, request, redirect, url_for
from database import connect_db, create_tables

app = Flask(__name__)
create_tables()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM beneficiaries")
    beneficiaries = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM volunteers")
    volunteers = cur.fetchone()[0]

    cur.execute("SELECT SUM(amount) FROM donations")
    donations = cur.fetchone()[0] or 0

    return render_template(
        "dashboard.html",
        beneficiaries=beneficiaries,
        volunteers=volunteers,
        donations=donations
    )

# ---------------- BENEFICIARIES ----------------
@app.route("/beneficiaries", methods=["GET", "POST"])
def beneficiaries():
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute(
            "INSERT INTO beneficiaries VALUES (NULL,?,?,?,?)",
            (
                request.form["name"],
                request.form["age"],
                request.form["education"],
                request.form["support"]
            )
        )
        conn.commit()

    cur.execute("SELECT * FROM beneficiaries")
    data = cur.fetchall()
    return render_template("beneficiaries.html", data=data)

@app.route("/delete-beneficiary/<int:id>")
def delete_beneficiary(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM beneficiaries WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("beneficiaries"))

# ---------------- VOLUNTEERS ----------------
@app.route("/volunteers", methods=["GET", "POST"])
def volunteers():
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute(
            "INSERT INTO volunteers VALUES (NULL,?,?,?)",
            (
                request.form["name"],
                request.form["role"],
                request.form["contact"]
            )
        )
        conn.commit()

    cur.execute("SELECT * FROM volunteers")
    data = cur.fetchall()
    return render_template("volunteers.html", data=data)

@app.route("/delete-volunteer/<int:id>")
def delete_volunteer(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM volunteers WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("volunteers"))

# ---------------- DONATIONS ----------------
@app.route("/donations", methods=["GET", "POST"])
def donations():
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute(
            "INSERT INTO donations VALUES (NULL,?,?,?)",
            (
                request.form["donor"],
                request.form["amount"],
                request.form["purpose"]
            )
        )
        conn.commit()

    cur.execute("SELECT * FROM donations")
    data = cur.fetchall()
    return render_template("donations.html", data=data)

@app.route("/delete-donation/<int:id>")
def delete_donation(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM donations WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("donations"))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
