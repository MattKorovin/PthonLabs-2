from flask import request

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        city = request.form["city"]
        date = request.form["date"]

        print(city)
        print(date)

    return render_template("index.html")