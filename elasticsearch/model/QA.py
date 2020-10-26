from datetime import datetime
from elasticsearch_dsl import Document, analyzer, Keyword, Text

german_analyzer = analyzer('german')
german_analyzer.char_filter=["html_strip"]

class QA(Document):
    url = Keyword()
    question = Text(analyzer=german_analyzer)
    question_text = Text(analyzer=german_analyzer)
    answer = Text(analyzer=german_analyzer)
    tags = Text(
        analyzer=german_analyzer,
        fields={'raw': Keyword()}
    )

    class Index:
        name = "law_qa"