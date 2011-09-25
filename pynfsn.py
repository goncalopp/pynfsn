import time
import string
import random
import hashlib
import urllib, urllib2


class NFSN_connection(object):
    '''This class contains only the bare functionality for doing API conformant requests'''
    SALT_CHARS= string.ascii_letters + string.digits
    BASE_URL= "https://api.nearlyfreespeech.net"

    def __init__(self, login, api_key):
        self.login, self.api_key= login, api_key

    def _salt(self):
        return "".join([random.choice(self.SALT_CHARS) for x in xrange(16)])

    def _timestamp(self):
        return str(int(time.time()))

    def _auth_header(self, url, body):
        if body is None:
            body=""
        l= self.login
        t= self._timestamp()
        s= self._salt()
        body_hash= hashlib.sha1(body).hexdigest()
        h_str= ";".join([l, t, s, self.api_key, url, body_hash])
        h= hashlib.sha1(h_str).hexdigest()
        return ";".join([l, t, s, h])

    def _headers(self, url, body):
        return {"X-NFSN-Authentication" : self._auth_header(url, body)}

    def _standard_request(self,url):
        r=urllib2.Request(self.BASE_URL+url)
        r.nfsn_url=url
        return r

    def _execute_http_method(self, request):
        request.headers=self._headers( request.nfsn_url, request.data)
        try:
            return urllib2.urlopen(request).read()
        except urllib2.HTTPError, e:
            raise Exception("error on GET: "+str(e.code)+str(e.read()))

    def get(self, url):
        return self._execute_http_method(self._standard_request(url))

    def post(self, url, parameters={}):
        r= self._standard_request(url)
        r.data= urllib.urlencode(parameters)
        return self._execute_http_method(r)

    def put(self, url, data):
        r= self._standard_request(url)
        r.data= data
        r.get_method = lambda: 'PUT'
        return self._execute_http_method(r)

class NFSN_instance(object):
    def __init__( self, instance_id, connection ):
        self.instance_id= instance_id
        self.connection= connection
        assert self.__class__.__name__.startswith("NFSN_")
        class_name= self.__class__.__name__[5:]
        self.base_url= "/"+ class_name +"/"+ instance_id

    def _property_get_set(self, url, set_to=None):
        if set_to is None:
            return self.connection.get( url )
        else:
            self.connection.put( url, str(set_to) )

class NFSN_account( NFSN_instance ):
    pass

class NFSN_database( NFSN_instance ):
    pass

class NFSN_dns( NFSN_instance ):
    pass

class NFSN_member( NFSN_instance ):
    pass

class NFSN_site( NFSN_instance ):
    pass

class NFSN(object):
    def __init__( self, login, api_key ):
        self.connection= NFSN_connection( login, api_key )
    def account( self, instance_id ):
        return NFSN_account( instance_id , self.connection)
    def database( self, instance_id ):
        return NFSN_database( instance_id , self.connection)
    def dns( self, instance_id ):
        return NFSN_dns( instance_id , self.connection)
    def member( self, instance_id ):
        return NFSN_member( instance_id , self.connection)
    def site( self, instance_id ):
        return NFSN_site( instance_id , self.connection)
