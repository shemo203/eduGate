from student import Student
from teacher import Teacher
from document import Document
from analyzer_api import Analyzer
from ThresholdChecker import ThresholdChecker
from submission import Submission

test_student = Student("1", "Abdi")
doc = Document("This is a dummy text")
test_teacher = Teacher("1", "Khaliq")

score = Analyzer(doc).analyze()
threshold_result = ThresholdChecker(0.5)
threshold_result.check_score(score)
submit = Submission(score, doc, test_teacher)







