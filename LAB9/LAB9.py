from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)


@app.route("/", methods=["GET", "POST"])
def index():
    city = ""
    date = ""
    visits = []

    if request.method == "POST":

        # Какая кнопка нажата
        action = request.form.get("action")

        if action == "clear":
            return render_template("index.html") # Без ничего
        # Иначе - продолжаем программу

        city = request.form.get("city", "").strip()
        date = request.form.get("date", "").strip()

        query = Visit.query
        query = query.order_by(Visit.city)

        if city:
            query = query.filter(Visit.city.ilike(f"%{city}%"))
            query = query.order_by(Visit.visit_date.desc())
        if date:
            query = query.filter(Visit.visit_date == datetime.strptime(date, "%Y-%m-%d").date())
            query = query.order_by(Visit.city)

        visits = query.all()

    return render_template("index.html", visits=visits, city=city, date=date)


app.run()