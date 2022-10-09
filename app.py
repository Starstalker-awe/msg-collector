from flask import Flask, render_template as render, redirect, request
from cs50 import SQL
from datetime import datetime
import os

if not os.path.exists("./db.db"):
	open("./db.db").close()

db = SQL("sqlite:///db.db")

db.execute("""
CREATE TABLE IF NOT EXISTS messages(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	addr VARCHAR(15),
	profile VARCHAR(200),
	message VARCHAR(2000),
	time TIMESTMAMP
);
""")
db.execute("""
CREATE TABLE IF NOT EXISTS visits(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	addr VARCHAR(15),
	time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		if len(str(request.remote_addr)) <= 15 and len(request.form["profile"]) <= 200 and len(request.form["message"]) <= 2000:
			db.execute("INSERT INTO messages (addr, profile, message, time) VALUES (?, ?, ?, ?)", 
				str(request.remote_addr), request.form["profile"], request.form["message"], datetime.now())
			return redirect("/thanks")
		else:
			return render("index.html", msg="Stop trying to break it, I'm not an idiot")
	db.execute("INSERT INTO visits (addr) VALUES (?)", request.remote_addr)
	return render("index.html")

@app.route("/thanks")
def thanks():
	return render("thanks.html")

if __name__ == "__main__":
	app.run(8080, DEBUG=False)
