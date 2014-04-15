import logging
import random
import urllib.request

from parser.common.utils import httpmanager
from parser.services.datasport.urls import COMMON_DATA

logger = logging.getLogger(__name__)



incorrect_login_body = """
You must login to perform this operation
"""
def incorrect_login():
    httpmanager.generate_response(
        httpmanager.STATUS_UNAUTHORIZED, httpmanager.CONTENT_HTML, incorrect_login_body)

def is_logged_in(session):
    if session is None:
        return False
    else:
        return httpmanager.validate_session_cookie(session['cookie'], 'user') and httpmanager.validate_session_user_id(session['user'])


def __login(session, args):
    if args is None:
            raise httpmanager.InvalidParametersException(
                "There are no arguments provided")
    # if args.has_key('user') and args.has_key('pass'):
    #        raise httpmanager.InvalidParametersException("Username and Password not provide")


    url_datasport = 'https://online.datasport.pl/zapisy/portal/hid/logon.php'
    url_post_data = {'login': args['user'], 'haslo': args['pass']}
    request_object = httpmanager.prepare_request_object(url_datasport, url_post_data,
                                                      httpmanager.HttpMethod.POST)
    if session is not None:
        return {'status': 'ok', 'info': 'Already logged in'}
    else:
        response = urllib.request.urlopen(request_object)
        cookie_string = response.headers.get("Set-Cookie")
        logger.debug("Cookie set in response: %s" % cookie_string)
        url_datasport = 'https://online.datasport.pl/zapisy/portal/index.php'
        url_post_data = {}
        request_object = httpmanager.prepare_request_object(
            url_datasport, url_post_data, httpmanager.HttpMethod.POST)
        request_object.add_header("Cookie", cookie_string)
        response = urllib.request.urlopen(request_object)
        if cookie_string is None:
            raise AuthException("Incorrect credentials provided")
        else:
            content = response.read().decode('cp1250')
            user_id = httpmanager.get_user_id(content)
            httpmanager.save_session(cookie_string, user_id)
            return {"status": "OK", "cookie": cookie_string}


def logout(session, args):
    logger.debug("Logging out")
    if session is None:
        raise httpmanager.InvalidSessionException("Invalid session")
    url_datasport = 'https://online.datasport.pl/zapisy/portal/hid/uAnlog.php'
    request_object = httpmanager.prepare_request_object(
        url_datasport, args, httpmanager.HttpMethod.GET)
    request_object.add_header("Cookie", session['cookie'])
    response = urllib.request.urlopen(request_object)

    cookie_string = response.headers.get("Set-Cookie")
    logger.debug("Response for logout %s" % cookie_string)
    if cookie_string is None:
        raise Exception("Logout failed")
    else:
        httpmanager.remove_session_data(
            SimpleCookie(session['cookie'])['user'].value)
        return {'status': 'OK', 'cookie': cookie_string}


def change_password(session, args):
    if session is None:
            raise Exception("Invalid session")

    url_datasport = 'https://online.datasport.pl/zapisy/portal/hid/passzap.php'
    url_post_data = {'id': session['user'], 'oldpass': args['old'],
                     'newpass1': args['new'], 'newpass2': args['new']}
    logger.debug("Data: %s" % url_post_data)
    request_object = httpmanager.prepare_request_object(
        url_datasport, url_post_data, httpmanager.HttpMethod.POST)
    request_object.add_header("Cookie", session['cookie'])
    response = urllib.request.urlopen(request_object)
    response_string = response.read()
    logger.debug("Response: %s" % response_string)
    if "ZAPISANO" not in response_string:
            raise Exception("Cannot change password")
    else:
        return {"status": "OK"}




def checkCredentials(args):
    if 'cookie' not in args:
        if 'login' not in args and 'haslo' not in args:
            headers = { 'Cookie': "" }
        else:
            login_resp = login(args)
            if login_resp != "":
                headers = { 'Cookie': login_resp }
            else:
                headers = { 'Cookie': "" }
    else:
        headers = { 'Cookie': 'user={0}'.format(args['cookie']) }

    return headers

def los():
    nb = round(random(0,12)*100000)
    return nb

def login(args):
    result = None
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    res, cont = httpmanager.httprequest(COMMON_DATA['LOGIN']['URL'], COMMON_DATA['LOGIN']['LOGIN_NEEDED'], args, 'POST', headers, urllib.parse.urlencode(args))
    if 'set-cookie' not in res:
        result = ""
    else:
        result = res['set-cookie']

    return (result)
