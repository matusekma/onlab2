from connect import connect
from model.QA_jura_forum import QAJuraForum

connect(hosts=['localhost'])

QAJuraForum.init()
