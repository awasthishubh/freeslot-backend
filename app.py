import sys
sys.path.insert(0, './routes/addons')
sys.path.insert(0, './routes')
sys.path.insert(0, './config')
sys.path.insert(0, './models')
from flask import Flask, jsonify, Response, request
import members, auth, keys, members_model
app = Flask(__name__)
from pymongo import MongoClient

app.config['UPLOAD_FOLDER'] = './tmp/'

db = MongoClient(keys.db).freeslots


@app.route('/',methods=['post','get'])
def index():
    return '<form action="/members" method="post" enctype="multipart/form-data"><input type="file" name="file" /><input type="submit"></form>'

members.routes(app,db)
auth.routes(app,db)

# @app.errorhandler(400)
# def err400(err):
#     print(err)
#     return (jsonify({'err': 'bad request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
