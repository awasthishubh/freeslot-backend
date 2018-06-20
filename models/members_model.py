from bson.objectid import ObjectId
def preturn(data):
    data['_id']=str(data['_id'])
    return data
class Members():
    def __init__(self, _db):
        self.db=_db
    def exists(self,reg,org):
        reg=reg.upper()
        org=org.lower()
        exists=self.db.members.find_one({'reg':reg, 'org':org})
        if(exists):
            return True
        else:
            return False


    def insert(self,data):
        data['reg']=data['reg'].upper()
        data['org']=data['org'].lower()
        # if(exists(db,data['reg'],data['org'])):
        #     return 500
        t3=[0,9,10,11,12,14,14,15,16,17,18,19,19,24]
        freeSlots=[]
        freeTimming=[]

        for i in range(7):
            day=data['slots'][i*13:(i+1)*13]
            freeSlot=[]
            for x in range(len(day)):
                if(not day[x]):
                    freeSlot.append(i*13+x)
            freeSlots.append(freeSlot)

            mod13=[x%13 for x in freeSlot]
            j=0
            freeT=[]
            while(j<len(mod13)):
                s=mod13[j]
                while (j<len(mod13)-1 and mod13[j]+1==mod13[j+1]):
                    j=j+1
                e=mod13[j]+1
                freeT.append((t3[s],t3[e]))
                j+=1
            freeTimming.append(freeT)

        data['freeTimming']=freeTimming
        data['freeSlots']=freeSlots
        del data['slots']
        data['verified']=False
        ins=self.db.members.insert_one(data)
        if(ins):
            data['_id']=str(data['_id'])
            return 200
        return 500

    def get(self,usid):
        usid=usid.lower()
        dataC=self.db.members.find({'org':usid})
        if(dataC):
            data=[]
            for i in dataC:
                i=preturn(i)
                data.append(i)
            return (data, 200)
        else:
            return (None, 404)

    def delete(self,usid, reg):
        usid=usid.lower()
        reg=reg.upper()
        data=self.db.members.delete_one({'org':usid, 'reg':reg})
        if(data.deleted_count):
            return 200
        else:
            return 404

    def verify(self, usid, reg):
        usid=usid.lower()
        reg=reg.upper()
        data=self.db.members.find_one({'org':usid, 'reg':reg})
        if(not data): return 404
        data=self.db.members.update({'org':usid, 'reg':reg},{'$set':{'verified':True}}, upsert=False)
        return 200
