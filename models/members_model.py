from bson.objectid import ObjectId
from pymongo import ASCENDING

def preturn(data):
    data['_id']=str(data['_id'])
    return data

def tocsv(data):
    data2="SNo,Reg,Name,Email,Phno,RoomNo\n"
    for i in data:
        data2+=str(data.index(i)+1)+','
        data2+=i['reg']+','
        data2+=i['name']+','
        data2+=i['email']+','
        data2+=i['phno']+','
        data2+=str(i['rmno'])+'\n'
    return data2

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
        slots=[]

        for i in range(7):
            day=data['slots'][i*13:(i+1)*13]
            day[5]=0
            del day[11]
            slot=[]
            for x in range(len(day)):
                if(day[x]):
                    slot.append(x)
            slots.append(slot)

        del data['slots']
        data['slots']=slots
        data['verified']=False
        ins=self.db.members.insert_one(data)
        if(ins):
            data['_id']=str(data['_id'])
            return 200
        return 500

    def insert2(self,data):
        data['reg']=data['reg'].upper()
        data['org']=data['org'].lower()
        data['verified']=False
        ins=self.db.members.insert_one(data)
        if(ins):
            data['_id']=str(data['_id'])
            return 200
        return 500

    def getmem(self,usid):
        usid=usid.lower()
        data=self.db.members.find({'org':usid, 'verified': True}).sort([("reg", ASCENDING)])
        if(data):
            verified=[]
            for i in data:
                i=preturn(i)
                i['visible']=True
                verified.append(i)
            return (verified, 200)
        else:
            return (None, 404)
    
    def getreq(self,usid):
        usid=usid.lower()
        data=self.db.members.find({'org':usid, 'verified': False}).sort([("reg", ASCENDING)])
        if(data):
            unverified=[]
            for i in data:
                i=preturn(i)
                i['visible']=True
                unverified.append(i)
            return (unverified, 200)
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

    
    def csv(self, usid):
        usid=usid.lower()
        dataC=self.db.members.find({'org':usid, 'verified': True}).sort([("reg", ASCENDING)])
        if(dataC):
            verified=[]
            for i in dataC:
                i=preturn(i)
                i['visible']=True
                verified.append(i)
            return (tocsv(verified), 200)
        else:
            return (None, 404)

    def freeMem(self,usid,day,slots):
        data=self.db.members.find({'org':usid, "slots."+str(day) : {"$not": {"$elemMatch" :{"$in": slots}}}}).sort([("reg", ASCENDING)])
        if(not data): return None
        members=[]
        for i in data:
            members.append(preturn(i))
        return members

    def mem(self, usid, reg):
        data=self.db.members.find_one({'org':usid, 'reg': reg})
        if(not data): return(None,404)
        else:
            return (preturn(data),200)


