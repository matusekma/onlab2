from flask import request, jsonify, Blueprint
from api.models.query import Query

search = Blueprint('search', __name__)


@search.route('/', methods=['GET'])
def query_questions():
    req_data = request.get_json()
    question = req_data['question']

    query = Query(question)
    return jsonify({question: query.question})


@search.errorhandler(404)
def page_not_found(error):
    return 'This url is not valid.'
