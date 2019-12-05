from flask import jsonify, Response, request
import jwt, functools, sys, hashlib
import os
import model
import datetime

def getYearReg(i):
    now=datetime.datetime.now()
    m=now.month
    t=int(str(now.year)[-2:])
    # if(m>=7):
    #     return str(t-i+1)
    return str(t-i)
#########Decorator for decoding jwt#############
def jwt_required(func):
    @functools.wraps(func)
    def jwt_func():
        if('Authorization' in request.headers.keys()):
            auth=(request.headers['Authorization']).split(' ')
            if(auth[0]=='Bearer'):
                # try:
                    payload=jwt.decode(auth[1],os.environ['jwt_secret'])
                    if(model.Organisations.exists(payload['usid'])==404):
                        return (jsonify({'err':'organisation not found'}), 401)
                    else:
                        return func(payload)
                # except:
                #     return (jsonify({'err':'invalid tokken'}), 401)
            else:
                return (jsonify({'err':'Bearer tokken missing'}), 401)
        else:
            return (jsonify({'err':'Bearer tokken missing'}), 401)
    return jwt_func
################################################

def routes(app):
    
    @app.route('/auth/org',methods=['get'])
    @jwt_required
    def orga(payload):
        data=model.Organisations.org(payload['usid'])
        gravatar=data['gravatar'] if 'gravatar' in data.keys() and data['gravatar'] else data['name'] #For random color
        hash=hashlib.md5(gravatar.encode()).hexdigest()
        data['dp']='https://www.gravatar.com/avatar/'+hash+'?d=retro&s=500'
        if(data):
            return jsonify({'details':data, 'status':200})
        return jsonify({'err':'Organisation not found', 'status':404})
#-----------
    @app.route('/auth/requests',methods=['get'])
    @jwt_required
    def reqget(payload):
        data=model.Requests.get(payload['usid'])
        if(data[1]==404):
            return(jsonify({'err':'No request found under your organisation', 'status':404}), 404)
        return (jsonify({'data':data[0], 'status':200}), 200)

    @app.route('/auth/members',methods=['get'])
    @jwt_required
    def memget(payload):
        if('reg' in request.args.keys()):
            reg=request.args['reg']
            data=model.Members.mem(payload['usid'], reg)
            if(data[1]==404):
                return(jsonify({'err':'No match found for usid', 'status':404}), 404)
            return (jsonify({'member':data[0], 'status':200}), 200)
        else:
            data=model.Members.getmem(payload['usid'])
            if(data[1]==404):
                return(jsonify({'err':'No member found under your organisation', 'status':404}), 404)
            return (jsonify({'data':data[0], 'status':200}), 200)

    @app.route('/auth/members',methods=['delete'])
    @jwt_required
    def memdel(payload):
        reg=request.args['reg']
        stat=model.Members.delete(payload['usid'], reg)
        if(stat==404):
            return(jsonify({'err':'No match found for usid', 'status':404}), 404)
        return (jsonify({'result':'deleted', 'status':200}), 200)
#----------
    @app.route('/auth/requests',methods=['delete'])
    @jwt_required
    def reqdel(payload):
        reg=request.args['reg']
        count=request.args['count']
        stat=model.Requests.delete(payload['usid'], reg, count)
        if(stat==404):
            return(jsonify({'err':'No match found for usid', 'status':404}), 404)
        return (jsonify({'result':'deleted', 'status':200}), 200)

    @app.route('/auth/requests',methods=['put'])
    @jwt_required
    def verify(payload):
        reg=request.args['reg']
        count=request.args['count']
        stat=model.Requests.verify(payload['usid'], reg, count)
        if(stat==404):
            return(jsonify({'err':'No match found for org and reg', 'status':404}), 404)
        else:
            return (jsonify({'result':'verified', 'status':200}), 200)

    @app.route('/auth/members/download',methods=['get'])
    @jwt_required
    def downloadcsv(payload):
        data=model.Members.csv(payload['usid'])
        resp = Response(data[0])
        resp.headers['Content-Type']="text/csv"
        resp.headers['Content-Disposition']='attachment; filename="'+payload['usid']+'_members.csv"'
        return resp
    
    @app.route('/auth/freemems',methods=['get'])
    @jwt_required
    def freemems(payload):
        start=int(request.args['start'])-8
        end=int(request.args['end'])-8
        day=int(request.args['day'])
        if(start>end or start>16 or end>16 or start==end): return (jsonify({'err':'Invalid start, end time', 'status':400}),400)
        array=[i for i in range(start,end)]
        data=model.Members.freeMem(payload['usid'],day,array)
        if(data): return jsonify({'members':data, 'status':200})
        else: return (jsonify({'err':'No member found', 'status':404}),404)

    # @app.route('/auth/member',methods=['get'])
    # @jwt_required
    # def mem(payload):
        
    
    @app.route('/auth/members/stats',methods=['get'])
    @jwt_required
    def memstat(payload):
        members=model.Members.getmem(payload['usid'])
        requests=model.Requests.get(payload['usid'])
        # return jsonify(members[0])
        stats={
            'requests':len(requests[0]),
            'members':0,
            'firstYr':0,
            'secondYr':0,
            'thirdYr':0,
            'fourthYr':0
        }
        for i in members[0]:
            stats['members']+=1
            if(i['reg'][0:2]==getYearReg(1)): stats['firstYr']+=1
            if(i['reg'][0:2]==getYearReg(2)): stats['secondYr']+=1
            if(i['reg'][0:2]==getYearReg(3)): stats['thirdYr']+=1
            if(i['reg'][0:2]==getYearReg(4)): stats['fourthYr']+=1
        return jsonify(stats)

    @app.route('/auth/members/timestat',methods=['get'])
    @jwt_required
    def freetime(payload):
        slots=[{i+8:0 for i in range(13)} for j in range(7)]
        members=model.Members.getmem(payload['usid'])
        for i in members[0]:
            for j in range(7):
                for k in i['slots'][j]:
                    # if(j==5):# and k==5):
                    #     print(i)
                    slots[j][k+8]+=1
                
        return jsonify(slots)

    @app.route('/auth/members/getplan',methods=['get'])
    @jwt_required
    def getplan(payload):
        start=int(request.args['start'])-8
        end=int(request.args['end'])-8
        day=int(request.args['day'])
        memType=int(request.args['mem'])

        if(start>end or start>16 or end>16 or start==end): return (jsonify({'err':'Invalid start, end time', 'status':400}),400)
        mems=[]
        reg=[]
        for i in range(start,end):
            mem=model.Members.suitFreeMem(payload['usid'],day,i,memType,reg)
            if(mem): reg.append(mem['reg'])
            mems.append(mem)
        return jsonify({"members":mems})


    

