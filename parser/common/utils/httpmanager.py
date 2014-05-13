import os
from http.cookies import SimpleCookie
import httplib2
import datetime
import re
import urllib.request
import json
import urllib
import pickle
import logging
logger = logging.getLogger("default")
logger.setLevel(logging.DEBUG)


STATUS_OK = 'Status: 200 OK'
STATUS_UNAUTHORIZED = 'Status: 403 Unauthorized'

CONTENT_HTML = "Content-type: text/html"
CONTENT_PLAIN = "Content-type: text/plain"
CONTENT_TYPE_MIME = "Content-Type: %s; name=\"%s\""
CONTENT_DISPOSITION = "Content-Disposition: %s; filename=\"%s\""

USER_AGENT = 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'

session_dir = os.curdir + "/.sessions/"
session_domain = 'gerritpi.no-ip.biz'
remote_session_dir = os.curdir + "/.remote_sessions/"


class AuthException(Exception):
        def __init__(self, message):
                Exception.__init__(self, message)


class InvalidSessionException(Exception):
        def __init__(self, message):
                Exception.__init__(self, message)


class InvalidParametersException(Exception):
        def __init__(self, message):
                Exception.__init__(self, message)


def generate_response(status_code, content_type, body, headers=[], cookie=None):
    print(status_code)
    print(content_type)
    if len(headers) > 0:
        print('\n'.join(headers))
    if not cookie is None:
        print(cookie)
    print("Length : %d" % len(body))
    print("")
    print(body)


def get_user_id(content):
        """
        Fetches user integer based id

        Search is based on regex of \"user=145\"
        @content Html response
        """
        match = re.search(r'id=(\d+)', content, flags=0)
        return match.group().split('=')[1]


def get_user_session_id():
    logger.debug("Getting user session id")
    remote_stored_cookie = SimpleCookie(os.environ.get('HTTP_COOKIE', None))
    logger.debug("Remote stored cookie: %s" % remote_stored_cookie)
    if remote_stored_cookie is None:
            return None
    if remote_stored_cookie.has_key('user'):
        logger.debug("Session id: %s" % remote_stored_cookie['user'].value)
        return remote_stored_cookie['user'].value
    else:
        logger.error("Session id not present")
        return None


class HttpMethod:
        POST, GET = range(0, 2)


def prepare_request_object(url, args, method):
    print(method)
    encoded_args = urllib.parse.urlencode(args)
    request_method = {
        HttpMethod.POST: urllib.request.Request(url, encoded_args.encode('utf-8')),
        HttpMethod.GET: urllib.request.Request(url+"?"+encoded_args),
        }

    request_object = request_method.get(method, urllib.request.Request(url+"?"+encoded_args))
    logger.debug("Url: %s Request method: %d Encoded arguments %s" % (url, method, encoded_args))
    return request_object


def load_local_session_data(session_id):
    if session_id is None:
            return None
    if session_id and os.path.exists(session_dir+session_id) and os.path.exists(session_dir+'.id.'+session_id):
        session_file = open(session_dir+session_id, 'rb')
        session_string = pickle.load(session_file)
        session_file.close()
        user_id = pickle.load(open(session_dir+'.id.'+session_id, "rb"))
        logger.debug("Cookie: %s UserId: %d" % (session_string, int(user_id)))
        return {'user': user_id, 'cookie': session_string}
    else:
        logger.error("Provided session %s not found" % session_id)
        return None


def get_cookie_attribute(cookie, cookie_value, attr_name):
        if cookie.has_key(cookie_value):
                if cookie[cookie_value].has_key(attr_name):
                        return cookie[cookie_value][attr_name]
                else:
                        return None
        return None


def validate_session_user_id(user_id):
        try:
                int_id = int(user_id)
                if int_id > 0:
                        return True
                else:
                        return False
        except:
                logger.error("Invalid user_id in session file")
                return False


def remove_session_data(session_id):
        os.remove(session_dir+session_id)
        os.remove(session_dir+'.id.'+session_id)


def validate_session_cookie(session, cookie_key):
        if session is None:
                logger.error("Session does not exist")
                return False
        session_cookie = SimpleCookie(session)
        expires_attribute = get_cookie_attribute(
            session_cookie, cookie_key, 'expires')
        expires = datetime.datetime.strptime(
            expires_attribute, "%a, %d-%b-%Y %H:%M:%S GMT") if expires_attribute is not None else None
        logger.debug("Expires %s Now %s" %
                     (expires, datetime.datetime.utcnow()))
        if expires is None:
                logger.error("There is no such cookie: %s" % session)
                return False
        # elif expires != datetime.datetime.utcnow():
        #        os.remove(session_dir+session_cookie[cookie_key].value)
        #        os.remove(session_dir+'.id.'+session_cookie[cookie_key].value)
        #        logger.error("Cookie has expired %s" % session_cookie[cookie_key]['expires'])
        #        return False
        else:
                logger.debug("Cookie %s is fine" % session_cookie[cookie_key])
                return True


def save_session(cookie_string, user_id):
    if not os.path.exists(session_dir):
            os.makedirs(session_dir)
    new_cookie = SimpleCookie(cookie_string)
    fCoockie = open(session_dir + new_cookie['user'].value, "wb")
    fUserId = open(session_dir + '.id.' + new_cookie['user'].value, "wb")
    pickle.dump(cookie_string, fCoockie)
    pickle.dump(user_id, fUserId)
    fCoockie.close()
    fUserId.close()



def call_api_func(function, args, login_needed):
        session = None
        response = None
        status = "OK"
        error_string = ""
        try:
                if login_needed:
                        logger.debug("Login needed: %r" % login_needed)
                        session = load_local_session_data(session_id)
                        logger.debug("Loaded session: %s" % session)
                        if session is None:
                                raise AuthException(
                                    "Session does not exist on server")
                        if not Auth.is_logged_in(session):
                                logger.debug("You are not logged in")
                                raise AuthException(
                                    "You are not authorized to perform this operation. Please login and try again")
                logger.debug("Session: %s Args: %s" % (session, args))
                response = function(session, args)
        except Exception as e:
                error_string = str(e)

        if response is None:
                logger.error(error_string)
                logger.error("Requested action cannot be performed")
                generate_response(STATUS_UNAUTHORIZED, CONTENT_HTML, json.dumps(
                    {'Status': 'Error', 'Error': error_string}, indent=4))
        else:
#                fp = open("json.txt", "w")
                json_dump = json.dumps(
                     {'Status': status, 'Data': response}, indent=4)

                generate_response(STATUS_OK, CONTENT_HTML, json_dump,
                                  cookie=SimpleCookie(response.get('cookie', None)))
#                fp.write(json_dump)


httpHandler = httplib2.Http('.cache', disable_ssl_certificate_validation=True)

def httprequest(url, login_needed, args, method="GET", headers=None, body=None):
    params = ""
#    if login_needed:
#        args['id'] = '1413'
#        args['los'] = '2015'
#
    for key, val in args.items():
        params +="&{0}={1}".format(key,val)
    logger.debug("Httprequest params: {0}".format(params))
    logger.debug("Httprequest headers: {0}".format(headers))
    logger.debug("Httprequest body: {0}".format(body))
    resp, content = httpHandler.request(url + '?' + params, method, headers=headers, body=body)
    return (resp, content.decode('cp1250'))
