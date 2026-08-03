from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "ngo_secret_key"

DATABASE = "database.db"

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)

        with open("database/schema.sql", "r") as f:
            conn.executescript(f.read())

        conn.commit()
        conn.close()
        print("Database Created Successfully!")

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin"] = username
            return redirect(url_for("dashboard"))

        else:
            return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():

    if "admin" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- Banner Management ----------------

@app.route('/banners')
def banners():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    banners = conn.execute(
        "SELECT * FROM banners ORDER BY display_order"
    ).fetchall()

    conn.close()

    return render_template("banners.html", banners=banners)


@app.route('/add_banner', methods=["GET", "POST"])
def add_banner():

    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        display_order = request.form["display_order"]
        status = request.form["status"]

        conn = sqlite3.connect(DATABASE)

        conn.execute("""
            INSERT INTO banners
            (title, description, image, display_order, status)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, "", display_order, status))

        conn.commit()
        conn.close()

        return redirect(url_for("banners"))

    return render_template("banners.html")


@app.route('/vision', methods=["GET", "POST"])
def vision():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        vision_title = request.form["vision_title"]
        vision_description = request.form["vision_description"]
        mission_title = request.form["mission_title"]
        mission_description = request.form["mission_description"]

        conn.execute("DELETE FROM vision_mission")

        conn.execute("""
            INSERT INTO vision_mission
            (vision_title, vision_description, mission_title, mission_description)
            VALUES (?, ?, ?, ?)
        """, (
            vision_title,
            vision_description,
            mission_title,
            mission_description
        ))

        conn.commit()

        conn.close()

        return redirect(url_for("vision"))


    data = conn.execute(
        "SELECT * FROM vision_mission LIMIT 1"
    ).fetchone()

    conn.close()

    return render_template("vision.html", data=data)

# ---------------- Statistics Management ----------------

@app.route('/statistics')
def statistics():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    statistics = conn.execute(
        "SELECT * FROM statistics ORDER BY display_order"
    ).fetchall()

    conn.close()

    return render_template("statistics.html", statistics=statistics)


@app.route('/add_statistic', methods=["POST"])
def add_statistic():

    if "admin" not in session:
        return redirect(url_for("login"))

    label = request.form["label"]
    value = request.form["value"]
    display_order = request.form["display_order"]
    status = request.form["status"]

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        INSERT INTO statistics
        (label, value, display_order, status)
        VALUES (?, ?, ?, ?)
    """, (
        label,
        value,
        display_order,
        status
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("statistics"))

# ---------------- Initiatives Management ----------------

@app.route('/initiatives')
def initiatives():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    initiatives = conn.execute(
        "SELECT * FROM initiatives ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("initiatives.html", initiatives=initiatives)


@app.route('/add_initiative', methods=["POST"])
def add_initiative():

    if "admin" not in session:
        return redirect(url_for("login"))

    title = request.form["title"]
    description = request.form["description"]
    status = request.form["status"]

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        INSERT INTO initiatives
        (title, description, image, status)
        VALUES (?, ?, ?, ?)
    """, (
        title,
        description,
        "",
        status
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("initiatives"))



if __name__ == "__main__":
    init_db()
    app.run(debug=True)



   