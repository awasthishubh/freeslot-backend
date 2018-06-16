import sys
sys.path.insert(0, './routes')
from flask import Flask, jsonify, Response, request
import members, auth

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './tmp/'

@app.route('/',methods=['post','get'])
def index():
    return '<form action="/members" method="post" enctype="multipart/form-data"><input type="file" name="file" /><input type="submit"></form>'

members.routes(app)
auth.routes(app)

# @app.errorhandler(400)
# def err400(err):
#     print(err)
#     return (jsonify({'err': 'bad request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
