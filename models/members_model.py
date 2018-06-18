from bson.objectid import ObjectId

def exists(db,reg,org):
    reg=reg.upper()
    org=org.lower()
    exists=db.members.find_one({'reg':reg, 'org':org})
    if(exists):
        return True
    else:
        return False


def insert(db,data):
    data['reg']=data['reg'].upper()
    data['org']=data['org'].lower()
    if(exists(db,data['reg'],data['org'])):
        return 500
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
    ins=db.members.insert_one(data)
    if(ins):
        data['_id']=str(data['_id'])
        return 200
    return 500
