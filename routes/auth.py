from flask import jsonify, Response, request
import jwt, functools

#########Decorator for decoding jwt#############
def jwt_required(func):
    @functools.wraps(func)
    def jwt_func():
        if('Authorization' in request.headers.keys()):
            auth=(request.headers['Authorization']).split(' ')
            if(auth[0]=='Bearer'):
                try:
                    payload=jsonify(jwt.decode(auth[1],'ss'))
                    return func(payload)
                except jwt.exceptions.DecodeError:#jwt.exceptions.DecodeError:
                    return (jsonify({'err':'invalid JSON'}), 400)
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
        paswd=request.form['passwd']
        # Authenticate user
        #
        #
        token=jwt.encode({'usid':usid},'ss').decode("utf-8")
        return jsonify({"access_token":token})

    @app.route('/auth/members',methods=['get'])
    @jwt_required
    def memauth(usid):
        return
