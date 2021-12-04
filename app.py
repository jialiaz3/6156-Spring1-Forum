from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging, re

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.ForumsResource.forum_service import ForumResource
from database_services.RDBService import RDBService as RDBService
from application_services.AppHTTPStatus import AppHTTPStatus

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# pagination data
OFFSET = 0
MAXLIMIT = 10

app = Flask(__name__)
CORS(app)

def handle_links(url, offset, limit):
    if "?" not in url:
        url += "?offset=" + str(offset) + "&limit=" + str(limit)
    else:
        if "offset" not in url:
            url = url + "&offset=" + str(offset)
        if "limit" not in url:
            url = url + "&limit=" + str(limit)
    links = []
    nexturl = re.sub("offset=\d+", "offset=" + str(offset + limit), url)
    prevurl = re.sub("offset=\d+", "offset=" + str(max(0, offset - limit)), url)
    links.append({"rel": "self", "href": url})
    links.append({"rel": "next", "href": nexturl})
    links.append({"rel": "prev", "href": prevurl})
    return links

@app.errorhandler(404)
def not_found(e):
    rsp = Response(response=json.dumps({"ERROR": "404 NOT FOUND"}, default=str, indent=4), status=404,
                   content_type="application/json")
    return rsp


@app.errorhandler(500)
def messy_error(e):
    print(e)
    rsp = Response(json.dumps({"ERROR": "500 WEIRD SERVER ERROR"}, default=str, indent=4), status=500,
                   content_type="application/json")
    return rsp

@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'

# @app.route("/forums/index", methods=["GET"])
# def get_forums_field():
#     if request.method == 'GET':
#         # /index?userID=2&gameID=20&fields=title,content
#         f_id = request.args.get("f_id")
#         userID = request.args.get("userID")
#         gameID = request.args.get("gameID")
#         fields = request.args.get("fields")
#         template = {}
#         if f_id:
#             template['f_id'] = f_id
#         if userID:
#             template['userID'] = userID
#         if gameID:
#             template['gameID'] = gameID
#         res = ForumResource.find_by_template_fields(fields,template)
#         resp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#         return resp

# /forums
@app.route('/forums', methods=['GET', 'POST'])
def get_forums():
    if request.method == 'GET':
        offset = int(request.args.get("offset", OFFSET))
        limit = int(request.args.get("limit", MAXLIMIT))
        if limit > MAXLIMIT:
            limit = MAXLIMIT
        query_parms = dict()
        arg_list = [i for i in request.args.keys()]
        for i in arg_list:
            if i.lower() != "offset" and i.lower() != "limit":
                query_parms[i] = request.args.get(i)
        data, exception_res = ForumResource.find_by_template(query_parms, limit, offset)
        links = handle_links(request.url, offset, limit)
        if data is not None:
            # res = {"data": data, "links": links}
            if len(data) == 0:
                # offset -= limit
                # print(offset)
                curr_len, _ = ForumResource.get_total_num("ForumInfo", "Forum")
                curr_len = curr_len[0]['COUNT(*)']
                offset = curr_len - curr_len % limit
                data, exception_res = ForumResource.find_by_template(query_parms, limit, offset)
            res = data
        else:
            res = data
        rsp = AppHTTPStatus().format_rsp(res, exception_res, method=request.method, path=request.path)
        return rsp
    elif request.method == 'POST':
        create_data = request.form
        if create_data:
            pass
        else:
            create_data = request.json
        res, exception_res = ForumResource.create(create_data)
        rsp = AppHTTPStatus().format_rsp(res, exception_res, method=request.method, path=request.path)
        return rsp


# /forums/<f_id>
@app.route('/forums/<f_id>', methods=['GET', 'PUT', 'DELETE'])
def get_forum_by_f_id(f_id):
    if request.method == 'GET':
        template = {"f_id": f_id}
        res, exception_res = ForumResource.find_by_template(template, 1, 0)
        rsp = AppHTTPStatus().format_rsp(res, exception_res, method=request.method, path=request.path)
        return rsp
    elif request.method == 'PUT':
        update_data = request.form
        if update_data:
            pass
        else:
            update_data = request.json
        select_data = {'f_id': f_id}
        res, exception_res = ForumResource.update(select_data, update_data)
        rsp = AppHTTPStatus().format_rsp(res, exception_res, method=request.method, path=request.path)
        return rsp
    elif request.method == 'DELETE':
        template = {"f_id": f_id}
        res, exception_res = ForumResource.delete(template)
        rsp = AppHTTPStatus().format_rsp(res, exception_res, method=request.method, path=request.path)
        return rsp


# /forums/<title>
@app.route('/forums/title/<title>', methods=['GET'])
def get_forum_by_title(title):
    if request.method == 'GET':
        template = {"title": title}
        res = ForumResource.find_by_template(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


# /forums/<f_id>/user
@app.route('/forums/<f_id>/users', methods=['GET'])
def get_linked_user(f_id):
    if request.method == 'GET':
        template = {"f_id": f_id}
        res = ForumResource.find_linked_user(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp

@app.route('/user/<userid>/forums', methods=['GET'])
def get_forums_from_userid(userid):
    if request.method == 'GET':
        template = {"userID": userid}
        offset = int(request.args.get("offset", OFFSET))
        limit = int(request.args.get("limit", MAXLIMIT))
        if limit > MAXLIMIT:
            limit = MAXLIMIT
        res, exception_res = ForumResource.find_by_template(template, limit, offset)
        rsp = AppHTTPStatus().format_rsp(res, exception_res, method=request.method, path=request.path)
        return rsp

if __name__ == '__main__':
    app.run(debug=False, port=5000)
