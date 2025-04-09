import teacher
class Submission:
    def __init__(self, isFlagged: bool, document, teacher: teacher):
        self.isFlagged = isFlagged
        self.document = document
        self.teacher = teacher

        