
class Organisations():
    def __init__(self, _db):
        self.db=_db
    def create(self, org, maintainer):
        data={
            'usid': org['usid'],
            'passwd': org['passwd'],
            'name': org['name'],
            'descr': org['descr'],
            'maintainer_name': maintainer['name'],
            'maintainer_email': maintainer['email'],
            'maintainer_photo': maintainer['picture'],
            'maintainer_id': maintainer['id']
        }

        exists=self.db.organisations.find_one({'usid':data['usid']})
        if(exists):
            return(data, 409)
        else:
            self.db.organisations.insert_one(data)
            data['_id']=str(data['_id'])
            return (data,200)

    def auth(self,data):
        user=self.db.organisations.find_one({'usid':data['usid']})
        if(user and user['passwd']==data['passwd']):
            return (data,200)
        else:
            return (None,401)

    def exists(self,usid):
        sts=self.db.organisations.find_one({'usid':usid})
        if(sts): return 200
        else: return 404
