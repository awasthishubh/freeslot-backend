from flask import Flask, jsonify, Response, request
import sys, string, random, os
from TT_SLOT import slotBits
# from preproc_beta import preproc
import model
import json

def routes(app):
    @app.route('/members',methods=['post'])
    def memindex():
        if(model.Organisations.exists(request.form['org'])==404):
            return(jsonify({'status':404, 'err':'Ogranisation not found'}),404)
        if(model.Members.exists(request.form['reg'],request.form['org'])):
            return(jsonify({'status':409, 'err':'User Already registered under the organisation'}),409)
        data=request.form
        f = request.files['timeTable']
        slots=slotBits(f.read())
        if(slots):
            details={
                'name':data['name'],
                'reg':data['reg'],
                'org':data['org'],
                'email':data['email'],
                'phno':data['phno'],
                'rmno':data['rmno'],
                'slots':slots
            }
            stat=model.Members.insert(details)
            if stat==500:
                return(jsonify({'status':500, 'err':'Internal Server Error'}),500)
            return(jsonify({'status':200, 'data':details}),200)
        return (jsonify({'err':'bad file'}),400)

    @app.route('/member',methods=['post'])
    def meminde():
        data=request.json
        if(model.Organisations.exists(data['org'])==404):
            return(jsonify({'status':404, 'err':'Ogranisation not found'}),404)
        if(model.Members.exists(data['reg'],data['org'])):
            return(jsonify({'status':409, 'err':'User Already registered under the organisation'}),409)
        details={
            'name':data['name'],
            'reg':data['reg'],
            'org':data['org'],
            'email':data['email'],
            'phno':data['phno'],
            'rmno':data['rmno'],
            'slots':data['slots']
        }
        stat=model.Members.insert2(details)
        if stat==500:
            return(jsonify({'status':500, 'err':'Internal Server Error'}),500)
        return(jsonify({'status':200, 'data':details}),200)

    @app.route('/test',methods=['post'])
    def test():
        return jsonify(slotBits(request.files['file'].read()))
        
    @app.route('/test',methods=['get'])
    def sd():
        return '<form action="/test" method="post" enctype="multipart/form-data"><input type="file" name="file" /><input type="submit"></form>'
