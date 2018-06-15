from flask import Flask, jsonify, Response, request
import sys
sys.path.insert(0, './routes/addons')
from preproc_beta import preproc
import string
import random
import os

def routes(app):
    @app.route('/members',methods=['post'])
    def memindex():
        name=''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        data=request.form
        f = request.files['timeTable']
        f.save('./tmp/'+name+'.png')
        slots=preproc('./tmp/'+name+'.png')
        os.remove('./tmp/'+name+'.png')

        freeSlots=[]
        for i in range(len(slots)):
            if(not slots[i]):
                freeSlots.append(i)

        details={
            'name':data['name'],
            'org':data['org'],
            'email':data['email'],
            'phno':data['phno'],
            'slots':freeSlots
        }

        return jsonify(details)
