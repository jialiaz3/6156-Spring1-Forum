from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging
import re 

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.ForumsResource.forum_service import ForumResource
from database_services.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# pagination data
OFFSET = 0
MAXLIMIT = 20

# help function for pagination
def handle_links(url, offset, limit):
    if "?" not in url:
        url += "?offset=" +str(offset)+"&limit=" +str(limit)
    else:
        if "offset" not in url:
            url = url + "&offset=" +str(offset)
        if "limit" not in url:
            url = url +"&limit=" +str(limit)
    links = []
    nexturl = re.sub("offset=\d+","offset="+str(offset+limit), url)
    prevurl = re.sub("offset=\d+","offset="+str(max(0,offset-limit)), url)
    links.append({"rel":"self","href":url})
    links.append({"rel":"next","href":nexturl})
    links.append({"rel":"prev","href":prevurl})
    return links

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


# /forum
@app.route('/forums', methods=['GET', 'POST'])
def get_forums():
    if request.method == 'GET':
        offset = int(request.args.get("offset", OFFSET))
        limit = int(request.args.get("limit", MAXLIMIT))
        if limit > MAXLIMIT:
            limit = MAXLIMIT
        data = ForumResource.find_by_template(None, limit, offset)
        links = handle_links(request.url, offset, limit)
        res ={"data":data,"links":links}
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
            update_data = request.json
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
        offset = int(request.args.get("offset", OFFSET))
        limit = int(request.args.get("limit", MAXLIMIT))
        if limit > MAXLIMIT:
            limit = MAXLIMIT
        data = ForumResource.find_by_template(template, limit, offset)
        links = handle_links(request.url, offset, limit)
        res ={"data":data,"links":links}
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
