from flask import Flask, jsonify, Response, request
import sys, string, random, os
from preproc_beta import preproc
import members_model

def routes(app,db):
    @app.route('/members',methods=['post'])
    def memindex():
        name=''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        data=request.form
        f = request.files['timeTable']
        f.save('./tmp/'+name+'.png')
        slots=preproc('./tmp/'+name+'.png')
        os.remove('./tmp/'+name+'.png')
        if(slots):
            freeSlots=[]
            for i in range(len(slots)):
                if(not slots[i]):
                    freeSlots.append(i)

            details={
                'name':data['name'],
                'reg':data['reg'],
                'org':data['org'],
                'email':data['email'],
                'phno':data['phno'],
                'slots':freeSlots
            }
            stat=members_model.insert(db,details)
            if stat==409:
                return(jsonify({'status':409, 'err':'User Already Exists'}),409)
            return(jsonify({'status':200, 'data':details}),200)
        return (jsonify({'err':'bad file'}),400)
