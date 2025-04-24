from flask import Flask, render_template, request
import os
from waitress import serve
UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def submit():
    if request.method == 'POST':  
        return submit_file()
    else:
        return render_template("submitpage.html")


def submit_file():
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return f"file {file.filename} returned sucessfully!"


if __name__ == "__main__":
    print("running")        
    app.run(debug=True)


