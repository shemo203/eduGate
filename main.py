from flask import Flask, render_template, request, redirect, url_for
import os
from waitress import serve
from transformers import pipeline
import pymupdf
import requests
from gradio_client import Client
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime, timezone
from flask import flash
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user, logout_user
from flask_mail import Mail, Message
from flask_login import login_required
from flask_login import current_user
from flask import send_from_directory

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///edugate')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view= "login"
login_manager.init_app(app)

# First load environment variables
load_dotenv()

# Then set mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("APP_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

secret_key = os.getenv("SECRET_KEY")
app.secret_key = secret_key


#Database models
class Student(UserMixin, db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    submissions = db.relationship('Submission', backref='student')

    def get_id(self):
        return f"student:{self.id}"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User{}>'.format(self.username)

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, nullable = False)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(50), nullable = False)
    submissions = db.relationship('Submission', backref='admin')


    def get_id(self):
        return f"admin:{self.id}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User{}>'.format(self.username)

class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime)
    score =  db.Column(db.Float)
    deadline = db.Column(db.DateTime)
    course_name = db.Column(db.String(50), nullable=False)
    student_ID = db.Column(db.Integer, db.ForeignKey('student.id'))
    admin_ID = db.Column(db.Integer, db.ForeignKey('admin.id'))
    documents = db.relationship('Document', secondary='submissionDocument')

class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key =True)
    file_type = db.Column(db.String(50))
    file_name = db.Column(db.String(50))
    size = db.Column(db.Integer)
    submissions = db.relationship('Submission', secondary= 'submissionDocument')

class SubmissionDocument(db.Model):
    __tablename__ = 'submissionDocument'
    submission_ID = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable = False, primary_key = True)
    document_ID = db.Column(db.Integer, db.ForeignKey('document.id'), nullable = False, primary_key = True)
    

@login_manager.user_loader
def load_user(user_key):
    if not user_key:
        return None
    user_type, user_id = user_key.split(":")
    if user_type == "student":
        return Student.query.get(int(user_id))
    elif user_type == "admin":
        return Admin.query.get(int(user_id))
    return None

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=['GET','POST'])
def landing():
    """Landing page - accessible without login"""
    if request.method == 'POST': 
        return submit_file()
    else:
        return render_template("landing.html")

@app.route("/studenthome")
@login_required
def studenthome():
        return render_template("studentlandingpage.html")
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            user = Student.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for(('submissions_page')))
            else:
                user = Admin.query.filter_by(username=username).first()
                if user and user.check_password(password):
                    login_user(user)
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash("Invalid username or password", "danger")
                    return redirect(url_for('login'))
        except Exception as e:
            flash (f"An error occured: {str(e)}", "danger")
            return redirect(url_for('login'))

    else:
        return render_template("loginpage.html")
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




@app.route("/admin_dashboard", methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    # Only allow admins
    if not isinstance(current_user, Admin):
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('login'))

    if request.method == "GET":
        try:
            admin_id = current_user.id
            submissions = Submission.query.filter(Submission.admin_ID == admin_id).all()
            students = Student.query.all()
            return render_template("adminsubpage.html", submissions=submissions, students=students)
        except Exception as e:
            flash(f"Error loading dashboard: {str(e)}", "danger")
            return render_template("adminsubpage.html", submissions=[], students=[])

    if request.method == "POST":
        try:
            course_name = request.form.get('course_name')
            student_ids = request.form.getlist('student_ids')
            deadline_str = request.form.get('deadline')

            # Validate form fields
            if not course_name or not student_ids or not deadline_str:
                flash("All fields are required.", "danger")
                return redirect(url_for('admin_dashboard'))

            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Invalid deadline format.", "danger")
                return redirect(url_for('admin_dashboard'))

            for student_id in student_ids:
                submission = Submission(
                    course_name=course_name,
                    student_ID=student_id,
                    admin_ID=current_user.id,
                    created_at=datetime.now(timezone.utc),
                    deadline=deadline
                )
                db.session.add(submission)
            db.session.commit()
            flash("Submissions created successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating submissions: {str(e)}", "danger")
            return redirect(url_for('admin_dashboard'))



    

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route("/submissions", methods=['GET','POST'])
@login_required
def submissions_page():
    if request.method =="GET":
        student = current_user
        student_id = student.id
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
@login_required
def view_submission(submission_id):
    if request.method == 'POST': 
        return submit_file(submission_id)
    else:
        submission = db.session.query(Submission).filter(Submission.id == submission_id).first()
        return render_template("submitpage.html", submission = submission)
    


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
 
@app.route("/debug/submissions")
def debug_submissions():
    result = []
    for sub in Submission.query.all():
        student = Student.query.get(sub.student_ID)
        admin = Admin.query.get(sub.admin_ID)
        result.append(
            f"Submission ID: {sub.id}, Course: {sub.course_name}, "
            f"Student: {student.username if student else 'N/A'}, "
            f"Admin: {admin.username if admin else 'N/A'}"
        )
    return "<br>".join(result)

def login_redirect():
    return None

@app.route("/contact", methods=["POST"])
def handle_contact():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        institution = request.form.get("institution")
        institution_type = request.form.get("institution_type")
        message = request.form.get("message")
        
        # Debug info to console
        print(f"Form submission: {name}, {email}, {institution}, {institution_type}")

 
        # Validate form data
        if not all([name, email, message]):
            flash("Please fill in all required fields", "danger")
            return redirect(url_for('landing'))
        
        # Create the email message using Flask-Mail
        app_receiver = os.getenv("MAIL_RECEIVER")
        
        msg = Message(
            subject=f"Contact Form: {name} from {institution} ({institution_type})",
            recipients=[app_receiver],
            sender=os.getenv("MAIL_USERNAME"),
            html=f"""
                <h3>New contact form submission</h3>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Institution:</strong> {institution}</p>
                <p><strong>Institution Type:</strong> {institution_type}</p>
                <p><strong>Message:</strong></p>
                <p>{message}</p>
                <hr>
                <p><em>This email was sent from the eduGate contact form.</em></p>
            """
        )
        

        try:
            mail.send(msg)
            flash("Tack för ditt meddelande! Vi återkommer så snart som möjligt.", "success")
        except Exception as e:
            print(f"Mail error: {str(e)}")
            flash("Ett problem uppstod när meddelandet skulle skickas. Vänligen försök igen.", "danger")
            
        return redirect(url_for('landing'))
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        flash(f"Ett fel uppstod: {str(e)}", "danger")
        return redirect(url_for('landing'))


def submit_file(submission_id):
    try:
        if 'file' not in request.files:
            flash("No file part in the request.", "danger")
            return redirect(request.url)
        file = request.files['file']
        submission = Submission.query.get(submission_id)
        if not submission:
            flash("Submission not found.", "danger")
            return redirect(request.url)
        
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        text = extract_pdf_content(file.filename)
        ai = analyze_text(text)
        print(ai)
        if ai[0] == "AI":
            return render_template("aisubmitpage.html", message = ai[1], submission_id = submission_id)
        else:
            document = Document(
            file_type=file.filename.split('.')[-1],
            size=os.path.getsize(os.path.join(UPLOAD_FOLDER, file.filename)),
            file_name=file.filename
            )
            submission.score = ai[1]
            submission.documents.append(document)
            db.session.add(document)
            db.session.commit()
            flash("Document submitted sucessfully!", "success")
            return redirect (url_for('submissions_page'))
    except Exception as e:
        flash(f"An error occured during submission: {str(e)}", "danger")
        return redirect(request.url)


def extract_pdf_content(pdf_input):
    doc = pymupdf.open(f"uploads/{pdf_input}")
    out = ""
    for page in doc:
        out += page.get_text()
    return out

def analyze_text(text):
    client = Client("yuchuantian/AIGC_text_detector_env3")
    result = client.predict(
		text)
    return result


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)


