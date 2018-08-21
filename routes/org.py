from flask import Flask, jsonify, Response, request, redirect
import jwt,requests
from keys import keys
import model
import hashlib

def routes(app):
    @app.route('/organisations',methods=['get'])
    def org():
        orgs=model.Organisations.all()
        return jsonify(orgs)

    @app.route('/organisations',methods=['post'])
    def orgReg():
        data={
            'usid': request.form['usid'],
            'passwd': hashlib.md5(request.form['passwd'].encode()).hexdigest(),
            'name': request.form['name'],
            'descr': request.form['descr'],
            'dp': request.form['dp'],
        }
        stat=model.Organisations.create(data)

        if stat[1]==409:
            return(jsonify({'status':409, 'err':'User Already Exists'}),409)
        token=jwt.encode({'usid':stat[0]['usid']},keys.jwt_secret).decode("utf-8")
        print(stat[0])
        return jsonify({'data':stat[0],'token':token})

    @app.route('/auth',methods=['get','post'])
    def auth():
        usid=request.form['usid']
        passwd=hashlib.md5(request.form['passwd'].encode()).hexdigest()
        print(request.form['passwd'],passwd)
        stat=model.Organisations.auth({'usid':usid, 'passwd':passwd})
        if(stat[1]!=200):
            return (jsonify({'err':'Invalid usid/password', 'status_code':401}), 401)
        token=jwt.encode({'usid':usid},keys.jwt_secret).decode("utf-8")
        return jsonify({"access_token":token, 'info':stat[0]})

    @app.route('/auth', methods=['put'])
    def authPut():
        data={}
        data['descr']=request.form['descr']
        data['dp']=request.form['dp']
        data['name']=request.form['name']
        data['passwd']=hashlib.md5(request.form['passwd'].encode()).hexdigest()
        data['usid']=request.form['usid']
        if('newPasswd' in request.form.keys() and request.form['newPasswd']):
            data['newPasswd']=hashlib.md5(request.form['newPasswd'].encode()).hexdigest()
        else: data['newPasswd']=data['passwd']
        stat=model.Organisations.update(data)
        if(stat):
            return (jsonify({'msg':'sucess'}),200)
        else:   return (jsonify({'err':'invalid usid/pass'}), 401)

    