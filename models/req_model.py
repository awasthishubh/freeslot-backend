from pymongo import ASCENDING
# import firebase
def preturn(data):
    data['_id']=str(data['_id'])
    return data


class Requests():
    def __init__(self, _db):
        self.db=_db
        
    def new(self, data):
        data['count']=self.db.requests.find({'org':data['org'],'reg':data['reg']}).count()+1
        id=self.db.requests.insert(data)
        del data['_id']
        if(id):
            return 200
        return 500

    def verify(self, usid, reg, count):
        usid=usid.lower()
        reg=reg.upper()
        data=self.db.requests.find_one({'org':usid, 'reg':reg, 'count':int(count)})
        if(not data): return 404
        del data['count']

        self.db.members.insert_one(data)

        for el in self.db.requests.find({'org':usid, 'reg':reg}):
            self.db.requests.delete_one({'_id':el['_id']})

        return 200

    def delete(self,usid, reg, count):
        usid=usid.lower()
        reg=reg.upper()
        data=self.db.requests.delete_one({'org':usid, 'reg':reg, 'count':int(count)})
        if(data.deleted_count):
            return 200
        else:
            return 404

    def get(self,usid):
        usid=usid.lower()
        data=self.db.requests.find({'org':usid}).sort([("reg", ASCENDING)])
        if(data):
            unverified=[]
            for i in data:
                i=preturn(i)
                i['visible']=True
                unverified.append(i)
            return (unverified, 200)
        else:
            return (None, 404)