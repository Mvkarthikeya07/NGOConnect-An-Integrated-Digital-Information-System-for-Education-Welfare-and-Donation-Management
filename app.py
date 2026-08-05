from functools import wraps

from flask import Flask, redirect, render_template, request, session, url_for

from database import (
    connect_db,
    create_tables,
    create_user,
    update_user_password,
    validate_user,
)

app = Flask(__name__)
app.secret_key = "ngoconnect-secret-key"
create_tables()


def render_login_page(active_box="login", **messages):
    form_data = messages.pop("form_data", {})
    return render_template(
        "login.html",
        active_box=active_box,
        form_data=form_data,
        **messages
    )


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped_view


# ---------------- AUTH ----------------
@app.route("/", methods=["GET"])
def login():
    if session.get("username"):
        return redirect(url_for("dashboard"))

    return render_login_page(active_box=request.args.get("box", "login"))


@app.route("/login", methods=["POST"])
def login_user():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if validate_user(username, password):
        session["username"] = username
        return redirect(url_for("dashboard"))

    return render_login_page(
        active_box="login",
        login_error="Invalid username or password",
        form_data={"login_username": username}
    )


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not username or len(password) < 4:
        return render_login_page(
            active_box="signup",
            signup_error="Username is required and password must be at least 4 characters.",
            form_data={"signup_username": username}
        )

    if password != confirm_password:
        return render_login_page(
            active_box="signup",
            signup_error="Passwords do not match.",
            form_data={"signup_username": username}
        )

    if not create_user(username, password):
        return render_login_page(
            active_box="signup",
            signup_error="That username already exists. Choose another one.",
            form_data={"signup_username": username}
        )

    return render_login_page(
        active_box="login",
        signup_success="Account created successfully. Please login.",
        form_data={"login_username": username}
    )


@app.route("/reset-password", methods=["POST"])
def reset_password():
    username = request.form.get("username", "").strip()
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not username:
        return render_login_page(
            active_box="reset",
            reset_error="Username is required."
        )

    if new_password != confirm_password:
        return render_login_page(
            active_box="reset",
            reset_error="Passwords do not match.",
            form_data={"reset_username": username}
        )

    if len(new_password) < 4:
        return render_login_page(
            active_box="reset",
            reset_error="Password must be at least 4 characters.",
            form_data={"reset_username": username}
        )

    if not update_user_password(username, new_password):
        return render_login_page(
            active_box="reset",
            reset_error="Username not found.",
            form_data={"reset_username": username}
        )

    return render_login_page(
        active_box="login",
        reset_success="Password reset successful. Please login.",
        form_data={"login_username": username}
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
@login_required
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
@login_required
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
@login_required
def delete_beneficiary(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM beneficiaries WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("beneficiaries"))


# ---------------- VOLUNTEERS ----------------
@app.route("/volunteers", methods=["GET", "POST"])
@login_required
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
@login_required
def delete_volunteer(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM volunteers WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("volunteers"))


# ---------------- DONATIONS ----------------
@app.route("/donations", methods=["GET", "POST"])
@login_required
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
@login_required
def delete_donation(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM donations WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("donations"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
