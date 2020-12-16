from elasticsearch_dsl import Document, analyzer, Text

german_analyzer = analyzer('german')
german_analyzer.char_filter=["html_strip"]

class QA(Document):
    question = Text(analyzer=german_analyzer)
    answer = Text(analyzer=german_analyzer)