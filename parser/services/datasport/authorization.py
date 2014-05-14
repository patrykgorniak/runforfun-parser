import logging
import random
import urllib.request
from pyquery import PyQuery

from parser.common.utils import httpmanager
from parser.services.datasport.urls import COMMON_DATA
from parser.services.datasport import accountmanager

logger = logging.getLogger("default")

#incorrect_login_body = """
#You must login to perform this operation
#"""
#def incorrect_login():
#    httpmanager.generate_response(
#        httpmanager.STATUS_UNAUTHORIZED, httpmanager.CONTENT_HTML, incorrect_login_body)
#
#def is_logged_in(session):
#    if session is None:
#        return False
#    else:
#        return httpmanager.validate_session_cookie(session['cookie'], 'user') and httpmanager.validate_session_user_id(session['user'])
#
#
#def __login(session, args):
#    if args is None:
#            raise httpmanager.InvalidParametersException(
#                "There are no arguments provided")
#    # if args.has_key('user') and args.has_key('pass'):
#    #        raise httpmanager.InvalidParametersException("Username and Password not provide")
#
#
#    url_datasport = 'https://online.datasport.pl/zapisy/portal/hid/logon.php'
#    url_post_data = {'login': args['user'], 'haslo': args['pass']}
#    request_object = httpmanager.prepare_request_object(url_datasport, url_post_data,
#                                                      httpmanager.HttpMethod.POST)
#    if session is not None:
#        return {'status': 'ok', 'info': 'Already logged in'}
#    else:
#        response = urllib.request.urlopen(request_object)
#        cookie_string = response.headers.get("Set-Cookie")
#        logger.debug("Cookie set in response: %s" % cookie_string)
#        url_datasport = 'https://online.datasport.pl/zapisy/portal/index.php'
#        url_post_data = {}
#        request_object = httpmanager.prepare_request_object(
#            url_datasport, url_post_data, httpmanager.HttpMethod.POST)
#        request_object.add_header("Cookie", cookie_string)
#        response = urllib.request.urlopen(request_object)
#        if cookie_string is None:
#            raise AuthException("Incorrect credentials provided")
#        else:
#            content = response.read().decode('cp1250')
#            user_id = httpmanager.get_user_id(content)
#            httpmanager.save_session(cookie_string, user_id)
#            return {"status": "OK", "cookie": cookie_string}
#
#
#def logout(session, args):
#    logger.debug("Logging out")
#    if session is None:
#        raise httpmanager.InvalidSessionException("Invalid session")
#    url_datasport = 'https://online.datasport.pl/zapisy/portal/hid/uAnlog.php'
#    request_object = httpmanager.prepare_request_object(
#        url_datasport, args, httpmanager.HttpMethod.GET)
#    request_object.add_header("Cookie", session['cookie'])
#    response = urllib.request.urlopen(request_object)
#
#    cookie_string = response.headers.get("Set-Cookie")
#    logger.debug("Response for logout %s" % cookie_string)
#    if cookie_string is None:
#        raise Exception("Logout failed")
#    else:
#        httpmanager.remove_session_data(
#            SimpleCookie(session['cookie'])['user'].value)
#        return {'status': 'OK', 'cookie': cookie_string}
#
#
#def change_password(session, args):
#    if session is None:
#            raise Exception("Invalid session")
#
#    url_datasport = 'https://online.datasport.pl/zapisy/portal/hid/passzap.php'
#    url_post_data = {'id': session['user'], 'oldpass': args['old'],
#                     'newpass1': args['new'], 'newpass2': args['new']}
#    logger.debug("Data: %s" % url_post_data)
#    request_object = httpmanager.prepare_request_object(
#        url_datasport, url_post_data, httpmanager.HttpMethod.POST)
#    request_object.add_header("Cookie", session['cookie'])
#    response = urllib.request.urlopen(request_object)
#    response_string = response.read()
#    logger.debug("Response: %s" % response_string)
#    if "ZAPISANO" not in response_string:
#            raise Exception("Cannot change password")
#    else:
#        return {"status": "OK"}



def __checkCredentials__(args):
    headers = {}
    if 'cookie' in args:
        headers = { 'Cookie': 'user={0}'.format(args['cookie']) }
        logger.debug("Cookie exists {0}".format(headers))
    else:
        if 'login' in args and 'haslo' in args:
            login_resp = __login__(args)
            if login_resp != "":
                headers = { 'Cookie': login_resp }
                logger.debug("Cookie exists {0}".format(headers))
            else:
                headers = { 'Cookie': "" }
                logger.debug("Could not login {0}".format(headers))
        else:
                headers = { 'Cookie': "" }
                logger.debug("Could not login: {0}".format(headers))
    return headers

def __login__(args):
    result = None
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    res, cont = httpmanager.httprequest(COMMON_DATA['LOGIN']['URL'], COMMON_DATA['LOGIN']['LOGIN_NEEDED'], args, 'POST', headers, urllib.parse.urlencode(args))

    if 'set-cookie' not in res:
        result = ""
    else:
        result = res['set-cookie']
    return (result)

def __isLoggedIn__(html):
    data = PyQuery(html)
    if data('div#right')('p')('input').attr('value').find('Wyloguj') != -1:
        return True
    else:
        return False

def login(args):
    headers = __checkCredentials__(args)

    if headers['Cookie']=="":
        logger.debug("Credential error.")
        return -1, headers
    else:
        logger.debug("Credential OK.")
        res, cont = httpmanager.httprequest(COMMON_DATA['USER_DATA']['URL'], COMMON_DATA['USER_DATA']['LOGIN_NEEDED'], {}, 'GET', headers)

        if not __isLoggedIn__(cont):
            logger.debug("Credential error.")
            return -1, headers

    return (accountmanager.get_id(cont), headers )

def los():
    nb = round(random.randint(1,11)*100000)
    return nb

