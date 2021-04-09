from bson.objectid import ObjectId
from pymongo import ASCENDING
import random
import datetime
# import firebase

def preturn(data):
    data['_id']=str(data['_id'])
    return data

def getMemRe(mem):
    if(mem==0): return '.*'
    now=datetime.datetime.now()
    year=int(str(now.year)[2:4])
    month=now.month
    if(month<7): return '^'+str(year-mem)
    return '^'+str(year-mem+1)

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
        ins=self.db.requests.insert_one(data)
        if(ins):
            data['_id']=str(data['_id'])
            return 200
        return 500

    def getmem(self,usid):
        usid=usid.lower()
        data=self.db.members.find({'org':usid}).sort([("reg", ASCENDING)])
        if(data):
            verified=[]
            for i in data:
                i=preturn(i)
                i['visible']=True
                verified.append(i)
            return (verified, 200)
        else:
            return (None, 404)
    
    def delete(self,usid, reg):
        usid=usid.lower()
        reg=reg.upper()
        id=self.db.members.find_one({'org':usid, 'reg':reg})['_id']
        print(str(id))
        data=self.db.members.delete_one({'org':usid, 'reg':reg})
        if(data.deleted_count):
            return 200
        else:
            return 404

    def csv(self, usid):
        usid=usid.lower()
        dataC=self.db.members.find({'org':usid}).sort([("reg", ASCENDING)])
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

    def suitFreeMem(self,usid,day,slot,memType,nin):
        daySlot="slots."+str(day)
        memType=getMemRe(memType)
        data=None
        data=self.db.members.find({
            "org":usid,
            daySlot:{"$not":{"$elemMatch":{"$eq":slot}}},
            "$and":[
                {"reg": {"$regex":memType}},
                {"reg": {"$nin":nin}}
            ],
            "$or":[
                {daySlot:{"$elemMatch":{"$eq":slot+1}}},
                {daySlot:{"$elemMatch":{"$eq":slot-1}}}
            ]
        })
        data=list(data)
        if(not data):
            data=self.db.members.find({
                "org":usid,
                daySlot:{"$not":{"$elemMatch":{"$eq":slot}}},
                "$and":[
                    {"reg": {"$regex":memType}},
                    {"reg": {"$nin":nin}}
                ]
            })
        data=list(data)
        if (not data):
            return {'forSlot':slot+8,'reg':None}
        memToreturn=data[random.randint(0,len(data)-1)]
        memToreturn['forSlot']=slot+8
        return preturn(memToreturn)


