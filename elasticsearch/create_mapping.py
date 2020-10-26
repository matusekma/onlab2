from model.QA import QA
from connect import connect

connect(hosts=['localhost'])

QA.init()

qa = QA(url="asd",
        question="asd", 
        question_text="Schön", 
        answer="Apfel", 
        tags=["Eins", "zwei"])

print(qa.save(index="law_qa"))

