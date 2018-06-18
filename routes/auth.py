from flask import jsonify, Response, request
import jwt, functools, sys
from keys import keys
import model

#########Decorator for decoding jwt#############
def jwt_required(func):
    @functools.wraps(func)
    def jwt_func():
        if('Authorization' in request.headers.keys()):
            auth=(request.headers['Authorization']).split(' ')
            if(auth[0]=='Bearer'):
                try:
                    payload=jwt.decode(auth[1],keys.jwt_secret)
                    if(model.Organisations.exists(payload['usid'])==404):
                        return (jsonify({'err':'organisation not found'}), 404)
                    else:
                        return func(payload)
                except jwt.exceptions.DecodeError:
                    return (jsonify({'err':'invalid tokken'}), 400)
            else:
                return (jsonify({'err':'Bearer tokken missing'}), 400)
        else:
            return (jsonify({'err':'Bearer tokken missing'}), 400)
    return jwt_func
################################################

def routes(app):
    @app.route('/auth',methods=['get','post'])
    def auth():
        usid=request.form['usid']
        passwd=request.form['passwd']
        stat=model.Organisations.auth({'usid':usid, 'passwd':passwd})
        if(stat[1]!=200):
            return (jsonify({'err':'Invalid usid/password', 'status_code':401}), 401)
        token=jwt.encode({'usid':usid},keys.jwt_secret).decode("utf-8")
        return jsonify({"access_token":token, 'info':stat[0]})


    @app.route('/auth/members',methods=['get'])
    @jwt_required
    def memauth(payload):
        return jsonify(payload)

    # @app.route('/auth/members',methods=['get'])
    # @jwt_required
    # def delmem():
    #     mem_reg=
    #
    #
    @app.route('/auth/org',methods=['get'])
    @jwt_required
    def orga(payload):
        return jsonify(model.Organisations.org(payload['usid']))
