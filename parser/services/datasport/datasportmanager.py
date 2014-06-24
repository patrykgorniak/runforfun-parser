import logging
from parser.services.datasport import eventlist
from parser.services.datasport.urls import COMMON_DATA
from parser.common.utils import httpmanager
from parser.services.datasport import authorization
from parser.services.datasport import accountmanager
from parser.common.utils.httpresponse import *
logger = logging.getLogger("default")


def get_interface(args=None):
    interface = {
        'get_events':get_events,
        'myaccount':myaccount,
        'get_user_events':get_user_events,
        'get_user_history_results':get_user_history_results,
        'change_pass':my_account_change_passwd,
        'log_out':log_out
    }
    return interface

def get_events(args=None):
    res, content = httpmanager.httprequest(COMMON_DATA['EVENT_LIST']['URL'], COMMON_DATA['LOGIN']['LOGIN_NEEDED'], args)
    event_list = eventlist.unpack_events(content, args)

    response = HttpResponse()
    response.set_status(res.reason)
    response.add_node('Data', event_list)
    return response


def myaccount(args):
    params = {}
    user_data = {}
    logger.debug("My account request.")
    ret, headers, content = authorization.login(args)

    if ret == -1:
        return HttpResponse()
    else:
        params['id'] = ret
        params['los'] = authorization.los()
        user_data['id'] = params['id']

        res, cont = httpmanager.httprequest(COMMON_DATA['CHANGE_USER_DATA']['URL'], COMMON_DATA['CHANGE_USER_DATA']['LOGIN_NEEDED'], params, httpmanager.HttpMethod.GET , headers)
        user_data.update(accountmanager.get_user_data(cont))

        response = HttpResponse()
        response.set_status(res.reason)
        response.add_node('Cookie', headers['Cookie'])
        response.add_node('Data', user_data)
        return response

def get_user_events(args):
    params = {}
    user_events = {}
    logger.debug("Get user events request.")
    ret, headers, cont = authorization.login(args)

    if ret == -1:
        return HttpResponse()

    user_events.update(accountmanager.get_user_events(cont))

    response = HttpResponse()
    response.set_status(HttpResponseStatus.OK)
    response.add_node("Data:", user_events)
    return response

def get_user_history_results(args):
    if 'id' not in args:
        return HttpResponse();

    params = {'id': args['id']}
    user_events = {}
    logger.debug("Get user events history request.")

    res, cont = httpmanager.httprequest(COMMON_DATA['USER_HISTORY_RESULTS']['URL'], COMMON_DATA['USER_HISTORY_RESULTS']['LOGIN_NEEDED'],params , httpmanager.HttpMethod.GET,  {})
    user_events.update(accountmanager.get_user_history_results(cont))

    response = HttpResponse()
    response.set_status(HttpResponseStatus.OK)
    response.add_node("Data:", user_events)
    return response

def my_account_change_passwd(args=None):
    params = {}
    logger.debug("my_account_change_passwd")
    if 'id' not in args:
        return HttpResponse();
    if 'oldpass' not in args:
        return HttpResponse()
    if 'newpass1' not in args:
        return HttpResponse()
    if 'newpass2' not in args:
        return HttpResponse()

    params['id'] = args['id']
    params['oldpass'] = args['oldpass']
    params['newpass1'] = args['newpass1']
    params['newpass2'] = args['newpass2']

    ret, headers, cont = authorization.login(args)

    if ret == -1:
        return HttpResponse()

    res, cont = httpmanager.httprequest(COMMON_DATA['CHANGE_PASS']['URL'], COMMON_DATA['CHANGE_PASS']['LOGIN_NEEDED'], params, httpmanager.HttpMethod.POST, headers)

    res = accountmanager.check_change_pass_result(cont)

    if res==False:
        return HttpResponse()

    response = HttpResponse()
    response.set_status(HttpResponseStatus.OK)
    return response

def log_out(args=None):
    if 'cookie' not in args:
        return HttpResponse()

    ret, headers, cont = authorization.login(args)

    if ret == -1:
        return HttpResponse()

    res, cont = httpmanager.httprequest(COMMON_DATA['LOGOUT']['URL'], COMMON_DATA['LOGOUT']['LOGIN_NEEDED'], headers = headers)

    response = HttpResponse()
    response.set_status(HttpResponseStatus.OK)
    return response
