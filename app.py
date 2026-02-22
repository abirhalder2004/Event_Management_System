from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="event_db"
)
cursor = db.cursor(dictionary=True)

@app.route("/")
def home():
    cursor.execute("SELECT * FROM events ORDER BY event_date ASC")
    events = cursor.fetchall()
    return render_template("index.html", events=events)


@app.route("/create")
def create_event_page():
    return render_template("create_event.html")


@app.route("/add-event", methods=["POST"])
def add_event():
    title = request.form["title"]
    description = request.form["description"]
    event_date = request.form["event_date"]

    cursor.execute(
        "INSERT INTO events (title, description, event_date) VALUES (%s, %s, %s)",
        (title, description, event_date)
    )
    db.commit()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_event(id):
    cursor.execute("DELETE FROM events WHERE id = %s", (id,))
    db.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
