from pymongo import MongoClient
import os

db = MongoClient(os.environ['db'])[os.environ['dbname']]

from members_model import Members
from org_model import Organisations
from req_model import Requests

Members= Members(db)
Organisations=Organisations(db)
Requests=Requests(db)