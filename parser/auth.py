import os
import http.cookies
import pickle
import parser.httpUtils as HttpUtils
#from Simple import SimpleCookie
import urllib.request
import http
import logging
logger = logging.getLogger(__name__)

incorrect_login_body = """
You must login to perform this operation
"""


def incorrect_login():
    HttpUtils.generate_response(
        HttpUtils.STATUS_UNAUTHORIZED, HttpUtils.CONTENT_HTML, incorrect_login_body)


def is_logged_in(session):
    if session is None:
        return False
    else:
        return HttpUtils.validate_session_cookie(session['cookie'], 'user') and HttpUtils.validate_session_user_id(session['user'])


def login(session, args):
    if args is None:
            raise HttpUtils.InvalidParametersException(
                "There are no arguments provided")
    # if args.has_key('user') and args.has_key('pass'):
    #        raise HttpUtils.InvalidParametersException("Username and Password not provide")
    url_datasport = 'https://online.datasport.pl/zapisy/portal/hid/logon.php'
    url_post_data = {'login': args['user'], 'haslo': args['pass']}
    request_object = HttpUtils.prepare_request_object(url_datasport, url_post_data,
                                                      HttpUtils.HttpMethod.POST)
    if session is not None:
        return {'status': 'ok', 'info': 'Already logged in'}
    else:
        response = urllib.request.urlopen(request_object)
        cookie_string = response.headers.get("Set-Cookie")
        logger.debug("Cookie set in response: %s" % cookie_string)
        url_datasport = 'https://online.datasport.pl/zapisy/portal/index.php'
        url_post_data = {}
        request_object = HttpUtils.prepare_request_object(
            url_datasport, url_post_data, HttpUtils.HttpMethod.POST)
        request_object.add_header("Cookie", cookie_string)
        response = urllib.request.urlopen(request_object)
        if cookie_string is None:
            raise AuthException("Incorrect credentials provided")
        else:
            content = response.read()
            user_id = HttpUtils.get_user_id(content)
            HttpUtils.save_session(cookie_string, user_id)
            return {"status": "OK", "cookie": cookie_string}


def logout(session, args):
    logger.debug("Logging out")
    if session is None:
        raise HttpUtils.InvalidSessionException("Invalid session")
    url_datasport = 'https://online.datasport.pl/zapisy/portal/hid/unlog.php'
    request_object = HttpUtils.prepare_request_object(
        url_datasport, args, HttpUtils.HttpMethod.GET)
    request_object.add_header("Cookie", session['cookie'])
    response = urllib.request.urlopen(request_object)

    cookie_string = response.headers.get("Set-Cookie")
    logger.debug("Response for logout %s" % cookie_string)
    if cookie_string is None:
        raise Exception("Logout failed")
    else:
        HttpUtils.remove_session_data(
            SimpleCookie(session['cookie'])['user'].value)
        return {'status': 'OK', 'cookie': cookie_string}


def change_password(session, args):
    if session is None:
            raise Exception("Invalid session")

    url_datasport = 'https://online.datasport.pl/zapisy/portal/hid/passzap.php'
    url_post_data = {'id': session['user'], 'oldpass': args['old'],
                     'newpass1': args['new'], 'newpass2': args['new']}
    logger.debug("Data: %s" % url_post_data)
    request_object = HttpUtils.prepare_request_object(
        url_datasport, url_post_data, HttpUtils.HttpMethod.POST)
    request_object.add_header("Cookie", session['cookie'])
    response = urllib.request.urlopen(request_object)
    response_string = response.read()
    logger.debug("Response: %s" % response_string)
    if "ZAPISANO" not in response_string:
            raise Exception("Cannot change password")
    else:
        return {"status": "OK"}
