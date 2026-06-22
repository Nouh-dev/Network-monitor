from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/assets")
def assets():
    return render_template("assets.html")

@app.route("/network")
def network():
    return render_template("network.html")

@app.route("/alerts")
def alerts():
    return render_template("alerts.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)

