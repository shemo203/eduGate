from flask import Flask, render_template
from waitress import serve

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def submit():
    return render_template("submitpage.html")


if __name__ == "__main__":
    print("running")        
    app.run(debug=True)