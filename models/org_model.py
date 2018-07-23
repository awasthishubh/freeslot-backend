def preturn(data):
    data['_id']=str(data['_id'])
    return data


class Organisations():
    def __init__(self, _db):
        self.db=_db
    def create(self, data):
        exists=self.db.organisations.find_one({'usid':data['usid']})
        if(exists):
            return(data, 409)
        else:
            self.db.organisations.insert_one(data)
            data['_id']=str(data['_id'])
            if('passwd' in data.keys()): del data['passwd']
            return (data,200)

    def auth(self,data):
        user=self.db.organisations.find_one({'usid':data['usid']})
        if(user and user['passwd']==data['passwd']):
            user['_id']=str(user['_id'])
            if('passwd' in data.keys()): del data['passwd']
            return (user,200)
        else:
            return (None,401)

    def update(self, data):
        user=self.db.organisations.update_one({
            'usid':data['usid'],
            'passwd':data['passwd']
        },{
            '$set': {
                'descr': data['descr'],
                'dp': data['dp'],
                'name': data['name'],
                'passwd': data['newPasswd']
            }
        }, upsert=False)

        return user.matched_count

    def exists(self,usid):
        sts=self.db.organisations.find_one({'usid':usid})
        if(sts): return 200
        else: return 404

    def all(self):
        orgsCursor=self.db.organisations.find({})
        orgs=[]
        for org in orgsCursor:
            orgs.append({'usid':org['usid'],'name':org['name']})
        return orgs

    def org(self, usid):
        data=self.db.organisations.find_one({'usid':usid})
        if('passwd' in data.keys()): del data['passwd']
        data['_id']=str(data['_id'])
        return data
