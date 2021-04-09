from environs import Env
env = Env()
env.read_env()
import sys
sys.path.insert(0, './models')
sys.path.insert(0, './config')
import model
# import firebase

def artoob(ar):
    ob={}
    for el in ar:
        id=str(el['_id'])
        del el['_id']
        ob[id]=el
    return ob

data={
    'members': artoob(model.db.members.find()),
    'organisations': artoob(model.db.organisations.find()),
    'requests': artoob(model.db.requests.find())
}

# firebase.db.reference('/').set(data)