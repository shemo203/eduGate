from flask import Flask, render_template, request
import os
from waitress import serve
from transformers import pipeline
import pymupdf
import requests
from gradio_client import Client
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Database models
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    submissions = db.relationship('Submission', backref='student') #handles the one to many relationship

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    submissions = db.relationship('Submission', backref='admin')

class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, nullable = False)
    score =  db.Column(db.Float)
    course_name = db.Column(db.String(50), nullable = False)
    student_ID = db.Column(db.Integer, db.ForeignKey('student.id'))
    admin_ID = db.Column(db.Integer, db.ForeignKey ('admin.id'))
    documents = db.relationship('Document', secondary='submissionDocument') #handles many to many relationship

class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key =True)
    file_type = db.Column(db.String(50))
    size = db.Column(db.Integer)
    submissions = db.relationship('Submission', secondary= 'submissionDocument')

class SubmissionDocument(db.Model):
    __tablename__ = 'submissionDocument'
    submission_ID = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable = False, primary_key = True)
    document_ID = db.Column(db.Integer, db.ForeignKey('document.id'), nullable = False, primary_key = True)
    

def add_test_data():
    # Create test students
    student1 = Student(name="John Doe")
    student2 = Student(name="Jane Smith")
    
    # Create test admin
    admin1 = Admin(name="Dr. Brown")
    
    # Create test document
    document1 = Document(file_type="pdf", size=1024)
    
    # Create test submission
    submission1 = Submission(
        created_at=datetime.utcnow(),
        score=85.5,
        course_name="Python Programming",
        student=student1,  # This sets the relationship
        admin=admin1,      # This sets the relationship
        documents=[document1]  # This sets the many-to-many relationship
    )
    
    # Add all objects to the session
    db.session.add_all([student1, student2, admin1, document1, submission1])
    
    # Commit the changes
    db.session.commit()

with app.app_context():
    db.create_all()
    # Check if we need to add test data
    if not Student.query.first():  # Only add if no students exist
        add_test_data()


UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

@app.route("/", methods=['GET','POST'])
def submit():
    if request.method == 'POST': 
        return submit_file()
    else:
        return render_template("submitpage.html")
    
@app.route("/admin-page", methods=['GET', 'POST'])
def admin_page():
    if request.method == "POST":
        return None
    else:
        return render_template("adminpage.html")
    

@app.route("/submissions", methods=['GET','POST'])
def submissions_page():
    if request.method =="GET":
        student_id = request.args.get('student_id')
        if student_id:
            submissions = db.session.query(Submission).filter(Submission.student_ID == student_id).all()
        else:
            submissions = db.session.query(Submission).all()
        return render_template("studentsubpage.html", submissions=submissions)
    if request.method == 'POST': 
        return None
    else:
        return render_template("studentsubpage.html", submissions=[])
    
@app.route("/submissions/<int:submission_id>", methods=['GET', 'POST'])
def view_submission(submission_id):
    if request.method == 'POST': 
        return submit_file(submission_id)
    else:
        return render_template("submitpage.html")
    


@app.route("/test-data")
def test_data():
    # Get all students
    students = Student.query.all()
    # Get all submissions
    submissions = Submission.query.all()
    
    # Print some information
    result = []
    for student in students:
        result.append(f"Student: {student.name}")
        for submission in student.submissions:
            result.append(f"  - Submission: {submission.course_name}")
            for doc in submission.documents:
                result.append(f"    - Document: {doc.file_type}")
    
    return "<br>".join(result)

def submit_file(submission_id):
    file = request.files['file']
    submission = Submission.query.get(submission_id)
    if not submission:
        return "Submission not found", 404
    
    document = Document(
        file_type=file.filename.split('.')[-1],
        size = 400
    )
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    submission.documents.append(document)

    db.session.add(document)
    db.session.commit()
    
    text = extract_pdf_content(file.filename)
    ai = analyze_text(text)
    if ai[0] == "AI":
        return render_template("aisubmitpage.html", message = ai[1])
    return f"Document submitted:"

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


def send_to_teacher():

    return None




if __name__ == "__main__":
    print("running")        
    app.run(debug=True)


