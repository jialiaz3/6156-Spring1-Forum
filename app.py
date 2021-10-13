from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.UsersResource.user_service import UserResource
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
@app.route('/forum', methods=['GET', 'POST'])
def get_forum():
    if request.method == 'GET':
        res = UserResource.find_by_template(None)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'POST':
        f_id = request.form['f_id']
        title = request.form['title']
        content = request.form['content']
        username = request.form['username']

        create_data = {"f_id": f_id, "title": title, "content": content, "username": username}
        res = UserResource.create(create_data)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


# /forum/<f_id>
@app.route('/forum/<f_id>', methods=['GET', 'DELETE'])
def get_forum_by_f_id(f_id):
    if request.method == 'GET':
        template = {"f_id": f_id}
        res = UserResource.find_by_template(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'DELETE':
        template = {"f_id": f_id}
        res = UserResource.delete(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


# /forum/<title>
@app.route('/forum/<title>', methods=['GET'])
def get_forum_by_title(title):
    if request.method == 'GET':
        template = {"title": title}
        res = UserResource.find_by_template(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
