from flask import Flask, jsonify, Response, request, redirect
import requests, keys
import org_model

def routes(app,db):
    @app.route('/oauth/')
    def oauth():
        data={
            'usid': request.args['usid'],
            'passwd': request.args['passwd'],
            'name': request.args['name'],
            'descr': request.args['descr']
        }
        for key in data.keys():
            data[key]=data[key].replace(' ','+')

        url='''https://accounts.google.com/o/oauth2/auth?
        login_hint='''+request.args['mail_id']+'''
        &state='''+str(data)+'''
        &response_type=code
        &scope=https://www.googleapis.com/auth/userinfo.email
        &client_id='''+keys.google['client_id']+'''
        &redirect_uri=http://localhost:5000/oauth/callback'''
        url = url.replace("\r","")
        url = url.replace("\n","")
        url = url.replace(" ","")
        return redirect(url)

    @app.route('/oauth/callback')
    @app.route('/oauth/callback')
    def callback():
        # return jsonify()
        data= {
                'client_id':keys.google['client_id'],
                'client_secret': keys.google['client_secret'],
                'grant_type': 'authorization_code',
                'code':request.args['code'],
                'redirect_uri': 'http://localhost:5000/oauth/callback',
            }

        r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)

        if(r.status_code != 200):
            print(r.text)
            return jsonify({'err':'Something went wrong', 'status': r.status_code})

        access_token=r.json()['access_token']
        t=requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={'Authorization': 'Bearer '+access_token})

        stat=org_model.create(db,eval(request.args['state']),t.json())

        if stat[1]==409:
            return(jsonify({'status':409, 'err':'User Already Exists'}),409)
        return(jsonify({'status':stat[1], 'data':stat[0]}),stat[1])
