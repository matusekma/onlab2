from flask import request, jsonify, Blueprint
import json
from werkzeug.exceptions import BadRequest
from api.models.query import Query

search = Blueprint('search', __name__)


@search.route('/', methods=['GET'])
def query_questions():
    req_data = request.get_json()

    if req_data is None or req_data['question'] is None:
        raise BadRequest(description="Request body should contain a question.")

    question = req_data['question']

    query = Query(question)
    return jsonify({'question': query.question})


# @search.errorhandler(BadRequest)
# def bad_request(error):
#     return json.dumps({
#         "code": 400,
#         "name": error.name,
#         "description": error.description,
#     }), 400


@search.errorhandler(404)
def page_not_found(error):
    return 'This url is not valid.'
