#!/usr/bin/env python3

import sys
import os
from environs import Env
env = Env()
env.read_env()
sys.path.insert(0, './routes/addons')
sys.path.insert(0, './routes')
sys.path.insert(0, './models')
from flask import Flask, jsonify, Response, request, send_from_directory
import members, auth, oauth, org
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './tmp/'


@app.route('/',methods=['post','get'])
def index2():
    response = send_from_directory(directory='./view', filename='index.html')
    return response

members.routes(app)
auth.routes(app)
oauth.routes(app)
org.routes(app)

# @app.errorhandler(500)
# def err500(err):
#     response = flask.Response(jsonify({'err': err}), status= 500)
#     response.headers['Access-Control-Allow-Headers']='Content-Type'
#     response.headers['Access-Control-Allow-Origin']='*'
#     return response

@app.after_request
def setcores(response):
    response.headers['Access-Control-Allow-Origin']='*'
    # response.headers['Access-Control-Allow-Headers']='Content-Type'
    response.headers["Access-Control-Allow-Headers"]= "authorization, Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    response.headers['Access-Control-Allow-Methods']='GET, PUT, POST, DELETE, PATCH, OPTIONS'
    response.headers["Access-Control-Allow-Credentials"]= "true"
    return response

if __name__ == '__main__':
    app.run(port=int(os.environ['PORT']), debug='debug' in os.environ)
