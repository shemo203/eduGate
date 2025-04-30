from flask import Flask, render_template, request
import os
from waitress import serve
from transformers import pipeline
import pymupdf
import requests
from gradio_client import Client

#reminders: use transformers and pumypdf for AI detection.

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
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
    text = extract_pdf_content(file.filename)
    ai = analyze_text(text)
    if ai[0] == "AI":
        return render_template("aisubmitpage.html", message = ai[1])
    return f"Document submitted: {analyze_text(text)}"

def extract_pdf_content(pdf_input):
    doc = pymupdf.open(f"uploads/{pdf_input}")
    out = ""
    for page in doc:
        out += page.get_text()
    return out

def analyze_text(text):
    client = Client("yuchuantian/AIGC_text_detector")
    result = client.predict(
		text,
		api_name="/predict_en")
    return result




if __name__ == "__main__":
    print("running")        
    app.run(debug=True)


