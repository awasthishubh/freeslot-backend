from bson.objectid import ObjectId

def insert(db,data):
    exists=db.members.find_one({'reg':data['reg']})
    if(exists):
        return 409
    else:
        db.members.insert_one(data)
        data['_id']=str(data['_id'])
        return 200
