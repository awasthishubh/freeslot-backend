from pymongo import MongoClient
from keys import keys

db = MongoClient(keys.db).freeslots

from members_model import Members
from org_model import Organisations

Members= Members(db)
Organisations=Organisations(db)
