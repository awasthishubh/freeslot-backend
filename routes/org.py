from flask import Flask, jsonify, Response, request, redirect
import jwt,requests
import model
import hashlib
import os

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
            'descr': request.form['descr'] if 'descr' in request.form.keys() else '',
            'gravatar': request.form['dp'] if 'dp' in request.form.keys() else '', #gravatar email
        }
        if 'gravatar' in request.form.keys(): data['gravatar']=request.form['gravatar']

        stat=model.Organisations.create(data)
        hash=hashlib.md5(data['gravatar'].encode()).hexdigest()
        data['dp']='https://www.gravatar.com/avatar/'+hash+'?d=retro&s=500'
        if stat[1]==409:
            return(jsonify({'status':409, 'err':'User Already Exists'}),409)
        token=jwt.encode({'usid':stat[0]['usid']},os.environ['jwt_secret'])
        print(stat[0])
        return jsonify({'data':stat[0],'token':token, 'status':200})

    @app.route('/auth',methods=['post'])
    def auth():
        usid=request.form['usid']
        passwd=hashlib.md5(request.form['passwd'].encode()).hexdigest()
        print(request.form['passwd'],passwd)
        stat=model.Organisations.auth({'usid':usid, 'passwd':passwd})
        if(stat[1]!=200):
            return (jsonify({'err':'Invalid usid/password', 'status':401}), 401)
        token=jwt.encode({'usid':usid},os.environ['jwt_secret'])
        
        gravatar=stat[0]['gravatar'] if 'gravatar' in stat[0].keys() and stat[0]['gravatar'] else stat[0]['name'] #For random color
        hash=hashlib.md5(gravatar.encode()).hexdigest()
        stat[0]['dp']='https://www.gravatar.com/avatar/'+hash+'?d=retro&s=500'

        return jsonify({"access_token":token, 'info':stat[0], 'status':200})

    @app.route('/auth', methods=['put'])
    def authPut():
        data={}
        data['descr']=request.form['descr']
        data['dp']=request.form['dp'] if 'dp' in request.form.keys() else request.form['gravatar']
        data['name']=request.form['name']
        data['passwd']=hashlib.md5(request.form['passwd'].encode()).hexdigest()
        data['usid']=request.form['usid']
        if('newPasswd' in request.form.keys() and request.form['newPasswd']):
            data['newPasswd']=hashlib.md5(request.form['newPasswd'].encode()).hexdigest()
        else: data['newPasswd']=data['passwd']
        stat=model.Organisations.update(data)
        if(stat):
            return (jsonify({'msg':'sucess', 'status':200}),200)
        else:   return (jsonify({'err':'invalid usid/pass', 'status':401}), 401)

    @app.route('/auth', methods=['patch'])
    def authPatch():
        allowedField=['name', 'descr','dp','gravatar','newPasswd','usid','passwd']
        data={k: v for k, v in request.form.items()}
        for i in list(data.keys()):
            if(i not in allowedField):
                return (jsonify({'err':'invalid field', 'status':400}),400)
            if(i=='dp'): 
                data['gravatar']=data['dp']
                del data['dp']

        stat=model.Organisations.auth({'usid':request.form['usid'], 'passwd':hashlib.md5(request.form['passwd'].encode()).hexdigest()})
        if(stat[1]!=200):
            return (jsonify({'err':'Invalid usid/password', 'status':401}), 401)
        

        del data['passwd']
        if('newPasswd' in list(request.form.keys())):
            data['passwd']=hashlib.md5(data['newPasswd'].encode()).hexdigest()
            del data['newPasswd']

        
        status=model.Organisations.patch(data)
        if(status):
            return(jsonify({'msg':'updated', 'status':200}))
        return(jsonify({'err':'Something\'s wrong', 'status':400}),400)    
    
    @app.route('/organisations/avbl', methods=['get'])
    def avbl():
        exists=model.Organisations.exists(request.args['usid'])
        if(exists==200):
            return (jsonify({'available': False}),409)
        return (jsonify({'available': True}),200)