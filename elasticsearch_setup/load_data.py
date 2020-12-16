from elasticsearch_dsl import Search
import json

from model.QA_jura_forum import QAJuraForum
from connect import connect

connect()

with open('./webscraping/data/jura_forum_1599411154273.json') as json_file:
    data = json.load(json_file)

for question_data in data:
    qa = QAJuraForum(
        url=question_data['url'],
        question=question_data['question'], 
        answer=question_data['answer'], 
        tags=question_data['tags'])
    qa.save(index='law_qa_jura_forum')