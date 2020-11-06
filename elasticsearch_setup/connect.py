from elasticsearch_dsl import connections

def connect(alias='default', hosts=['localhost']):
    connections.create_connection(alias=alias, hosts=hosts, timeout=60)