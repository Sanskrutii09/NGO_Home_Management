from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "ngo_secret_key"

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

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

# ---------------- Our Story Management ----------------

@app.route('/our_story', methods=["GET", "POST"])
def our_story():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        content = request.form["content"]

        conn.execute("DELETE FROM our_story")

        conn.execute("""
            INSERT INTO our_story (content)
            VALUES (?)
        """, (content,))

        conn.commit()

        return redirect(url_for("our_story"))

    story = conn.execute(
        "SELECT * FROM our_story LIMIT 1"
    ).fetchone()

    conn.close()

    return render_template("our_story.html", story=story)

@app.route("/core-values", methods=["GET", "POST"])
def core_values():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        conn.execute(
            "INSERT INTO core_values(title, description) VALUES (?, ?)",
            (title, description)
        )

        conn.commit()

    values = conn.execute(
        "SELECT * FROM core_values"
    ).fetchall()

    conn.close()

    return render_template(
        "core_values.html",
        values=values
    )

@app.route("/edit-core-value/<int:id>", methods=["GET","POST"])
def edit_core_value(id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        conn.execute("""
            UPDATE core_values
            SET title=?, description=?
            WHERE id=?
        """,
        (title, description, id))

        conn.commit()

        conn.close()

        return redirect(url_for("core_values"))


    value = conn.execute(
        "SELECT * FROM core_values WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_core_value.html",
        value=value
    )

@app.route("/delete-core-value/<int:id>")
def delete_core_value(id):

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "DELETE FROM core_values WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("core_values"))

@app.route("/programs", methods=["GET", "POST"])
def programs():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]

        conn.execute("""
            INSERT INTO programs (name, description)
            VALUES (?, ?)
        """, (name, description))

        conn.commit()

    programs = conn.execute(
        "SELECT * FROM programs"
    ).fetchall()

    conn.close()

    return render_template(
        "programs.html",
        programs=programs
    )

@app.route("/edit-program/<int:id>", methods=["GET", "POST"])
def edit_program(id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]

        conn.execute("""
            UPDATE programs
            SET name=?, description=?
            WHERE id=?
        """, (name, description, id))

        conn.commit()
        conn.close()

        return redirect(url_for("programs"))

    program = conn.execute(
        "SELECT * FROM programs WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_program.html",
        program=program
    )

@app.route("/delete-program/<int:id>")
def delete_program(id):

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "DELETE FROM programs WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("programs"))

@app.route("/team-members", methods=["GET", "POST"])
def team_members():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        name = request.form["name"]
        designation = request.form["designation"]

        conn.execute("""
            INSERT INTO team_members (name, designation, image)
            VALUES (?, ?, ?)
        """, (name, designation, ""))

        conn.commit()

    members = conn.execute(
        "SELECT * FROM team_members"
    ).fetchall()

    conn.close()

    return render_template(
        "team_members.html",
        members=members
    )

@app.route("/edit-team-member/<int:id>", methods=["GET", "POST"])
def edit_team_member(id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        name = request.form["name"]
        designation = request.form["designation"]

        conn.execute("""
            UPDATE team_members
            SET name=?, designation=?
            WHERE id=?
        """, (name, designation, id))

        conn.commit()
        conn.close()

        return redirect(url_for("team_members"))

    member = conn.execute(
        "SELECT * FROM team_members WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_team_member.html",
        member=member
    )

@app.route("/delete-team-member/<int:id>")
def delete_team_member(id):

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "DELETE FROM team_members WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("team_members"))

@app.route("/about")
def about():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    story = conn.execute(
        "SELECT * FROM our_story LIMIT 1"
    ).fetchone()

    values = conn.execute(
        "SELECT * FROM core_values"
    ).fetchall()

    programs = conn.execute(
        "SELECT * FROM programs"
    ).fetchall()

    members = conn.execute(
        "SELECT * FROM team_members"
    ).fetchall()

    conn.close()

    return render_template(
        "about.html",
        story=story,
        values=values,
        programs=programs,
        members=members
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

    