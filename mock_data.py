from main import app, db, Student, Admin, Submission, Document, SubmissionDocument
from datetime import datetime, timedelta
import random

def create_mock_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create mock students
        students = [
            Student(name="John Smith"),
            Student(name="Emma Johnson"),
            Student(name="Michael Brown"),
            Student(name="Sarah Davis"),
            Student(name="David Wilson")
        ]
        
        # Create mock admins
        admins = [
            Admin(name="Dr. Robert Anderson"),
            Admin(name="Prof. Lisa Martinez"),
            Admin(name="Dr. James Thompson")
        ]
    
        # Create mock documents
        documents = [
            Document(file_type="pdf", size=1024),
            Document(file_type="pdf", size=2048),
            Document(file_type="pdf", size=3072),
            Document(file_type="pdf", size=4096),
            Document(file_type="pdf", size=5120)
        ]
        
        # Create mock submissions
        courses = ["Python Programming", "Data Structures", "Web Development", "Database Systems", "Machine Learning"]
        submissions = []
        
        # Generate submissions for each student
        for student in students:
            # Each student gets 2-4 submissions
            num_submissions = random.randint(2, 4)
            for _ in range(num_submissions):
                submission = Submission(
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                    score=random.uniform(60.0, 100.0),
                    course_name=random.choice(courses),
                    student=student,
                    admin=random.choice(admins),
                    documents=[random.choice(documents)]
                )
                submissions.append(submission)
        
        db.session.add_all(students)
        db.session.add_all(admins)
        db.session.add_all(documents)
        db.session.add_all(submissions)
    
        db.session.commit()
        
        print("Mock data created successfully!")
        print(f"Created {len(students)} students")
        print(f"Created {len(admins)} admins")
        print(f"Created {len(documents)} documents")
        print(f"Created {len(submissions)} submissions")

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