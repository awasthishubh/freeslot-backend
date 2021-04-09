# import firebase

def preturn(data):
    data['_id']=str(data['_id'])
    return data


class Organisations():
    def __init__(self, _db):
        self.db=_db
    def create(self, data):
        exists=self.db.organisations.find_one({'usid':data['usid'].lower()})
        if(exists):
            return(data, 409)
        else:
            self.db.organisations.insert_one(data)
            data['_id']=str(data['_id'])
            if('passwd' in data.keys()): del data['passwd']
            return (data,200)

    def auth(self,data):
        user=self.db.organisations.find_one({'usid':data['usid'].lower(), 'passwd': data['passwd']})
        if(user):
            user['_id']=str(user['_id'])
            if('passwd' in user.keys()): del user['passwd']
            return (user,200)
        else:
            return (None,401)

    def update(self, data):
        id=self.db.organisations.find_one({
            'usid':data['usid'].lower(),
            'passwd':data['passwd']
        })['_id']
        if(not id): return 0
        data={
            'descr': data['descr'],
            'dp': data['dp'],
            'name': data['name'],
            'passwd': data['newPasswd']
        }
        user=self.db.organisations.update_one({'_id':id},{'$set': data}, upsert=False)
        return user.matched_count

    def exists(self,usid):
        sts=self.db.organisations.find_one({'usid':usid.lower()})
        if(sts): return 200
        else: return 404

    def all(self):
        orgsCursor=self.db.organisations.find({})
        orgs=[]
        for org in orgsCursor:
            orgs.append({'usid':org['usid'].lower(),'name':org['name']})
        return orgs

    def org(self, usid):
        data=self.db.organisations.find_one({'usid':usid.lower()})
        if('passwd' in data.keys()): del data['passwd']
        data['_id']=str(data['_id'])
        return data

    def patch(self,data):
        id=self.db.organisations.find_one({
            'usid':data['usid'].lower(),
        })['_id']
        if(not id): return 0
        print(111111111,id)
        user=self.db.organisations.update_one({'_id':id},{'$set': data}, upsert=False)
        return user.matched_count