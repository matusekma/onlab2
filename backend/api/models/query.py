class Query:
    def __init__(self, question, category=None) -> None:
        super().__init__()
        self.question = question
        self.category = category
