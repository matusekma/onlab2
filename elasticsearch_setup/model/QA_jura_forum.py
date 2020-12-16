from elasticsearch_dsl import analyzer, Keyword, Text

from QA_base import QA, german_analyzer

class QAJuraForum(QA):
    url = Keyword()
    tags = Text(
        analyzer=german_analyzer,
        fields={'raw': Keyword()}
    )

    class Index:
        name = "law_qa_jura_forum"
