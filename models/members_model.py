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

    def get(self,usid):
        usid=usid.lower()
        dataC=self.db.members.find({'org':usid, 'verified': True})
        dataV=self.db.members.find({'org':usid, 'verified': False})
        if(dataC or dataV):
            verified=[]
            for i in dataC:
                i=preturn(i)
                i['visible']=True
                verified.append(i)
            unverified=[]
            for i in dataV:
                i=preturn(i)
                i['visible']=True
                unverified.append(i)
            return ({'verified':verified,'unverified':unverified}, 200)
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

    def getmem(self, usid, start, end, point):
        dataC=self.db.members.find({'org':usid, 'verified': True})
        if(dataC):
            data=[]
            data2=[]
            for i in dataC:
                i=preturn(i)
                # print(i)
                print(start,end,point)
                print(i['slots'][point])
                okay=True
                for j in range(start, end+1):
                    if(j in i['slots'][point]):
                        okay=False
                        break
                if(okay):
                    data.append(i)
                else: data2.append(i)

            return ({'availableMem':data}, 200)
        else:
            return (None, 404)

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


