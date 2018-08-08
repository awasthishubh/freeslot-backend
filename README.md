# FreeSlot
### Route:   '/organisations'
##### Method: 
* GET: 
    * Get all the registered organisation
----

### Route:   '/members'
##### Method: 
* POST: 
    * Post details of a member for registration
    Required Fields:
        * name
        * reg
        * org
        * email
        * phno
        * rmno
----

### Route:   '/auth'
##### Method: 
* GET or POST: 
    * Login for an organisation
    Required Fields
        * usid
        * passwd
* PUT:
    * Create or Update an organisation
    Required Fields:
        * usid
        * passwd
        * name
        * descr
        * dp
        * newPasswd // Required only for updating, not for registration

On sucessful login, a `JSON token` will be returned which need to be send as `bearer token` in subsequent requests

----
### Route:   '/auth/org' `// Bearer token required`
##### Method: 
* GET:  
    * Get details of organisation
----

### Route:   '/auth/members'  `// Bearer token required`
##### Method: 
* GET:
    * Get All members of authenticated organisation
* PUT:
    * Send reg=17XXX2345 as query parameter
    * Accept/Verify a member
* DELETE
    * Send reg=17XXX2345 as query parameter
    * Delete a member
----

### Route:   '/auth/members/download' `// Bearer token required`
##### Method: 
* GET:  
    * Download details of all members as an CSV file
----
