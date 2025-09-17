from main import app, db, Student, Admin, Submission, Document, SubmissionDocument
from datetime import datetime, timedelta
import random

def create_mock_data():
    with app.app_context():
        print("Clearing existing data...")
        Student.query.delete()
        Admin.query.delete()
        Submission.query.delete()
        Document.query.delete()
        # Clear junction table if it exists
        db.session.execute(db.text("DELETE FROM submissionDocument"))
        db.session.commit()
        # Create mock students
        students = [
            Student(username="Steve", name="Steve"),
            Student(username="Josh", name="Josh"),
            Student(username="Ashley", name="Ashley"),
            Student(username="Beyonce", name="Beyonce"),
            Student(username="Justin", name="Justin"),
            Student(username="Ye", name="Ye"),
            Student(username="Marshall", name="Marshall"),
            Student(username="Benjamin", name="Benjamin"),
            Student(username="Erik", name="Erik"),
            Student(username="Julia", name="Julia"),
            Student(username="Alice", name="Alice"),
            Student(username="Sofia", name="Sofia"),
            Student(username="Sten", name="Sten"),
            Student(username="Axel", name="Axel"),
            Student(username="Oscar", name="Oscar"),
            Student(username="Sixten", name="Sixten"),
            Student(username="Alicia", name="Alicia"),
            Student(username="Meghan", name="Meghan"),
            Student(username="Marcus", name="Marcus"),
            Student(username="Stefan", name="Stefan"),
            Student(username="Lukas", name="Lukas"),
            Student(username="Linnea", name="Linnea"),
            Student(username="Jonathan", name="Jonathan")
        ]
        for student in students:
            student.set_password("testpass")  # All students have the same password for testing
        
        # Create mock admins
        admins = [
            Admin(username="Daniel", name="Daniel"),
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