import sys
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
    return '<form action="/members" method="post" enctype="multipart/form-data"><input type="file" name="file" /><input type="submit"></form>'

members.routes(app)
auth.routes(app)
oauth.routes(app)

# @app.errorhandler(404)
# def err400(err):
#     print(err)
#     return (jsonify({'err': 'Not found'}), 404)

@app.after_request
def setcores(response):
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Access-Control-Allow-Headers']='Content-Type'
    return response

if __name__ == '__main__':
    app.run(debug=True)
