class Document:
    def __init__(self, content: str, language: str = "en"):
        self.content = content
        self.language = language


    def get_content(self):
        return self.content