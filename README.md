# FreeSlot
### Route:&emsp;'/organisations'
##### Method: 
* POST:
    * Register an organisation
    * Required Fields: ``name``, ``usid``, ``passwd``
    * Optional Fields: ``descr``, ``dp``
* GET: 
    * Get all the registered organisation
    
On sucessful registration, a `JSON token` will be returned which need to be send as&emsp; `Bearer token` in subsequent requests for authorisation

----

### Route:&emsp;'/organisations/avbl'
##### Method: 

* GET: 
    * Checks the availability of usid
    * send usid as parameter in url
----

### Route:&emsp;'/auth'
##### Method: 
* POST: 
    * Login for an organisation
    * Required Fields (as form-data or url-encoded in request body)
        * usid
        * passwd
* PATCH:
    * Update details of organisation
    * Send ```usid```, ```passwd``` along with the fields that need to be updated
    * Fields that can be send/updated: ``name``, ``descr``, ``dp``, ``newPasswd``(for updating passwd)

On sucessful login, a `JSON token` will be returned which need to be send as&emsp; `Bearer token` in subsequent requests for authorisation

----
### Route:&emsp;'/members'
##### Method: 
* POST: 
    * Post details of a member for registration
    * Required Fields (to be send as form data):
        * name
        * reg
        * org
        * email
        * phno
        * rmno
        * timeTable `Screenshot of time table`
----
### Route:&emsp;'/auth/org'&emsp; `Bearer token required`
##### Method: 
* GET:  
    * Get details of authenticated organisation
----

### Route:&emsp;'/auth/members' &emsp; `Bearer token required`
##### Method: 
* GET:
    * Get details of members of authenticated organisation
    * if u need to get details of a particular member, send `?reg=17XXX23X` as query parameter
* DELETE
    * Delete a member or request
    * Send `reg=17XXX2345` as query parameter
    
----
### Route:&emsp;'/auth/requests' &emsp; `Bearer token required`
##### Method: 
* GET:
    * Get All pending requests of authenticated organisation
* PUT:
    * Accept/Verify a member
    * Send `reg=17XXX2345` as query parameter
---
### Route:&emsp;'/auth/freemems'&emsp; `Bearer token required`
##### Method: 
* GET:  
    * Get all the members who are free during specified day/time
    * Following fields (with integer as value) need to be send as query parameter
        * `start`: Start hour of time interval in 24hr format
        * `end`: End hour of time interval in 24hr format
        * `day`: Day of the week `0 for monday, 6 for sunday`

eg. if you need to find members who are free on wednesday from 11:00 AM to 4:00 PM
send `?start=11&end=16&day=2` as query parameter

----
### Route:&emsp;'/auth/members/stats'&emsp; `Bearer token required`
##### Method: 
* GET:  
    * Get statistics about registered member of your organisation
----
### Route:&emsp;'/auth/members/download'&emsp; `Bearer token required`
##### Method: 
* GET:  
    * Download details of all members as an CSV file
----
