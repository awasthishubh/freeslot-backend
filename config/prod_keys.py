import os
jwt_secret=os.environ['jwt_secret']
db=os.environ['db']

google={
    'client_id': os.environ['g_client_id'],
    'client_secret': os.environ['g_client_secret'],
    'callback': os.environ['g_callback']
}
