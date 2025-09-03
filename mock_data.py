from main import app, db, Student, Admin, Submission, Document, SubmissionDocument
from datetime import datetime, timedelta
import random

def create_mock_data():
    with app.app_context():
        # Create mock students
        students = [
            Student(username="john", name="John Smith"),
            Student(username="emma", name="Emma Johnson"),
            Student(username="michael", name="Michael Brown"),
            Student(username="sarah", name="Sarah Davis"),
            Student(username="david", name="David Wilson")
        ]
        for student in students:
            student.set_password("testpass")  # All students have the same password for testing
        
        # Create mock admins
        admins = [
            Admin(username="robert", name="Dr. Robert Anderson"),
            Admin(username="lisa", name="Prof. Lisa Martinez"),
            Admin(username="james", name="Dr. James Thompson")
        ]
        
        for admin in admins:
            admin.set_password("adminpass")  # All admins have
        
        db.session.add_all(students)
        db.session.add_all(admins)
    
        db.session.commit()
        
        print("Mock data created successfully!")
        print(f"Created {len(students)} students")
        print(f"Created {len(admins)} admins")

def view_mock_data():
    """View all data in the database"""
    with app.app_context():
        print("\n=== Students ===")
        students = Student.query.all()
        for student in students:
            print(f"ID: {student.id}, Name: {student.name}")
            for submission in student.submissions:
                print(f"  - Submission: {submission.course_name} (Score: {submission.score})")
        
        print("\n=== Admins ===")
        admins = Admin.query.all()
        for admin in admins:
            print(f"ID: {admin.id}, Name: {admin.name}")
        
        print("\n=== Documents ===")
        documents = Document.query.all()
        for doc in documents:
            print(f"ID: {doc.id}, Type: {doc.file_type}, Size: {doc.size}")

if __name__ == "__main__":
    create_mock_data()
    view_mock_data() 