from flask import Flask, jsonify, Response, request
import sys, string, random, os
from TT_SLOT import slotBits
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
                'name':data['name'].title(),
                'reg':data['reg'].upper(),
                'org':data['org'].lower(),
                'email':data['email'].lower(),
                'phno':data['phno'],
                'rmno':data['rmno'],
                'slots':slots
            }
            stat=model.Members.insert(details)
            if stat==500:
                return(jsonify({'status':500, 'err':'Internal Server Error'}),500)
            return(jsonify({'status':200, 'data':details}),200)
        return (jsonify({'err':'bad file'}),400)
#--------------
    @app.route('/member',methods=['post'])
    def meminde():
        data=request.json
        details={
            'name':data['name'].strip().title(),
            'reg':data['reg'].strip().upper(),
            'org':data['org'].strip().lower(),
            'email':data['email'].strip().lower(),
            'phno':data['phno'].strip(),
            'rmno':data['rmno'].strip().title(),
            'slots':data['slots']
        }
        if(model.Organisations.exists(details['org'])==404):
            return(jsonify({'status':404, 'err':'Ogranisation not found'}),404)
        if(model.Members.exists(details['reg'],details['org'])):
            return(jsonify({'status':409, 'err':'User Already registered under the organisation'}),409)
        
        stat=model.Requests.new(details)
        if stat==500:
            return(jsonify({'status':500, 'err':'Internal Server Error'}),500)
        return(jsonify({'status':200, 'data':details}),200)
    
    @app.route('/parseimg',methods=['post'])
    def memnde():
        f = request.files['timeTable']
        slots=slotBits(f.read())
        if(slots):
            numberedSlots=[]
            for i in range(7):
                day=slots[i*13:(i+1)*13]
                day[5]=0
                del day[11]
                slot=[]
                for x in range(len(day)):
                    if(day[x]):
                        slot.append(x)
                numberedSlots.append(slot)
            return (jsonify({'slots':numberedSlots}),200)
        return (jsonify({'err':'bad file'}),400)


    @app.route('/currentsem',methods=['get'])
    def currentsem():
        return 'VL2018195'

    @app.route('/test',methods=['post'])
    def test():
        return jsonify(slotBits(request.files['file'].read()))
        
    @app.route('/test',methods=['get'])
    def sd():
        return '<form action="/test" method="post" enctype="multipart/form-data"><input type="file" name="file" /><input type="submit"></form>'

    @app.route('/testDB',methods=['get'])
    def testdb():
        print((model.db.members.find({'org':'acsm'}).count())+1)
        return ''
