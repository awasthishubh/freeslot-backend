import sys
import os
sys.path.insert(0, './routes/addons')
sys.path.insert(0, './routes')
sys.path.insert(0, './config')
sys.path.insert(0, './models')
from flask import Flask, jsonify, Response, request
import members, auth, oauth
app = Flask(__name__)
from keys import keys

app.config['UPLOAD_FOLDER'] = './tmp/'

@app.route('/',methods=['post','get'])
def index():
    return '<form action="/test" method="post" enctype="multipart/form-data"><input type="file" name="file" /><input type="submit"></form>'

members.routes(app)
auth.routes(app)
oauth.routes(app)

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

debug=False
if('HEROKU' not in os.environ):
    debug=True

if __name__ == '__main__':
    app.run(debug=debug)
