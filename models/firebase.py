import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import model
import json
import os

cred = credentials.Certificate(json.loads(os.environ['fbAuth']))

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://freeslot-1.firebaseio.com/'
})

class Members:
    def __init__(self):
        self.ref = db.reference('/members')
    
    def insert(self,id, arr):
        newA={i:arr[i] for i in arr if i!='_id'}
        self.ref.child(id).set(newA)
    
    def delete(self,id):
        self.ref.child(id).delete()

class Requests:
    def __init__(self):
        self.ref = db.reference('/requests')
    
    def insert(self,id, arr):
        newA={i:arr[i] for i in arr if i!='_id'}
        print(newA)
        self.ref.child(id).set(newA)
    
    def delete(self,id):
        self.ref.child(id).delete()

class Organisations:
    def __init__(self):
        self.ref = db.reference('/organisations')
    
    def insert(self,id, arr):
        newA={i:arr[i] for i in arr if i!='_id'}
        self.ref.child(id).set(newA)
    
    def delete(self,id):
        self.ref.child(id).delete()

    def update(self,id, data):
        print(data)
        for i in data:
            print(i)
            self.ref.child(id).child(i).set(data[i])

def setFirebase():
    data={
        members: model.db.find({})
    }
