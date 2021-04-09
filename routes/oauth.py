from flask import Flask, jsonify, Response, request, redirect
import jwt,requests
import model
import hashlib
import os

def routes(app):
    @app.route('/oauth/')
    def oauth():
        data={
            'usid': request.args['usid'],
            'passwd': hashlib.md5(request.args['passwd'].encode()).hexdigest(),
            'name': request.args['name'],
            'descr': request.args['descr'],
            'dp': request.args['dp'],
        }
        stat=model.Organisations.create(data)

        if stat[1]==409:
            return(jsonify({'status':409, 'err':'User Already Exists'}),409)
        token=jwt.encode({'usid':stat[0]['usid']},os.environ['jwt_secret'])

        return ("""
        <script>
            opener.postMessage({token:'"""+token+"""'},"*");
            window.close()
        </script>
         """)
        # for key in data.keys():
        #     data[key]=data[key].replace(' ','+')

        # url='''https://accounts.google.com/o/oauth2/auth?
        # login_hint='''+request.args['mail_id']+'''
        # &state='''+str(data)+'''
        # &response_type=code
        # &scope=https://www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/plus.login
        # &client_id='''+keys.google['client_id']+'''
        # &redirect_uri='''+keys.google['callback']
        # url = url.replace("\r","")
        # url = url.replace("\n","")
        # url = url.replace(" ","")
        # return redirect(url)
 
    # @app.route('/oauth/callback')
    # def callback():
    #     # return jsonify()
    #     data= {
    #             'client_id':keys.google['client_id'],
    #             'client_secret': keys.google['client_secret'],
    #             'grant_type': 'authorization_code',
    #             'code':request.args['code'],
    #             'redirect_uri': keys.google['callback'],
    #         }

    #     r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)

    #     if(r.status_code != 200):
    #         print(r.text)
    #         return jsonify({'err':'Something went wrong', 'status': r.status_code})

    #     access_token=r.json()['access_token']
    #     t=requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={'Authorization': 'Bearer '+access_token})
    #     state=eval(request.args['state'])
    #     stat=model.Organisations.create(state,t.json())

    #     if stat[1]==409:
    #         return(jsonify({'status':409, 'err':'User Already Exists'}),409)
    #     stat[0]['token']=jwt.encode({'usid':stat[0]['usid']},keys.jwt_secret)
    #     url=state['redirect']+"#token="+stat[0]['token']
    #     return ("""
    #     <script>
    #         opener.postMessage({token:'"""+stat[0]['token']+"""'},"*");
    #         window.close()
    #     </script>
    #      """)
    #     # return(jsonify({'status':stat[1], 'data':stat[0]}),stat[1])
