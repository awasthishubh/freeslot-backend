import os
if('HEROKU' in os.environ):
    import prod_keys as keys
else:
    import local_keys as keys
