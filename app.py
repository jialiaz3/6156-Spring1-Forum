from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.ForumsResource.forum_service import ForumResource
from database_services.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


# /forum
@app.route('/forums', methods=['GET', 'POST'])
def get_forums():
    if request.method == 'GET':
        res = ForumResource.find_by_template(None)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'POST':
        create_data = request.form
        if create_data:
            pass
        else:
            create_data = request.json[0]
        res = ForumResource.create(create_data)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


# /forum/<f_id>
@app.route('/forums/<f_id>', methods=['GET', 'PUT', 'DELETE'])
def get_forum_by_f_id(f_id):
    if request.method == 'GET':
        template = {"f_id": f_id}
        res = ForumResource.find_by_template(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'PUT':
        update_data = request.form
        if update_data:
            pass
        else:
            update_data = request.json[0]
        select_data = {'f_id': f_id}
        res = ForumResource.update(select_data, update_data)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'DELETE':
        template = {"f_id": f_id}
        res = ForumResource.delete(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


# /forum/<title>
@app.route('/forums/title/<title>', methods=['GET'])
def get_forum_by_title(title):
    if request.method == 'GET':
        template = {"title": title}
        res = ForumResource.find_by_template(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
