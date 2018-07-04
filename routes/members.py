from flask import Flask, jsonify, Response, request
import sys, string, random, os
from TT_SLOT import findSlot
import model

def routes(app):
    @app.route('/members',methods=['post'])
    def memindex():
        if(model.Organisations.exists(request.form['org'])==404):
            return(jsonify({'status':404, 'err':'Ogranisation not found'}),409)
        if(model.Members.exists(request.form['reg'],request.form['org'])):
            return(jsonify({'status':409, 'err':'User Already registered under the organisation'}),409)
        name=''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        data=request.form
        f = request.files['timeTable']
        f.save('./tmp/'+name+'.png')
        slots=findSlot('./tmp/'+name+'.png')
        os.remove('./tmp/'+name+'.png')
        if(slots):
            details={
                'name':data['name'],
                'reg':data['reg'],
                'org':data['org'],
                'email':data['email'],
                'phno':data['phno'],
                'slots':slots
            }
            stat=model.Members.insert(details)
            if stat==500:
                return(jsonify({'status':500, 'err':'Internal Server Error'}),500)
            return(jsonify({'status':200, 'data':details}),200)
        return (jsonify({'err':'bad file'}),400)

    @app.route('/organisations',methods=['get'])
    def org():
        orgs=model.Organisations.all()
        return jsonify(orgs)
