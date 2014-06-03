from parser.services.datasport import eventlist
from parser.services.datasport.urls import COMMON_DATA
from parser.common.utils import httpmanager
from parser.services.datasport import authorization
from parser.services.datasport import accountmanager
import urllib
import logging
import json
from parser.common.utils.httpresponse import HttpResponse
logger = logging.getLogger("default")


def get_events(args=None):
    res, content = httpmanager.httprequest(COMMON_DATA['EVENT_LIST']['URL'], COMMON_DATA['LOGIN']['LOGIN_NEEDED'], args)
    event_list = eventlist.unpack_events(content, args)

    response = HttpResponse()
    response.add_node('Status', res.reason)
    response.add_node('Data', event_list)
    return response


def myaccount(args):
    params = {}
    user_data = {}
    logger.debug("My account request.")
    ret, headers = authorization.login(args)

    if ret == -1:
        return HttpResponse.error()
    else:
        params['id'] = ret
        params['los'] = authorization.los()
        user_data['id'] = params['id']

        res, cont = httpmanager.httprequest(COMMON_DATA['CHANGE_USER_DATA']['URL'], COMMON_DATA['CHANGE_USER_DATA']['LOGIN_NEEDED'], params, 'GET', headers)
        user_data.update(accountmanager.get_user_data(cont))

        response = HttpResponse()
        response.add_node('Status', res.reason)
        response.add_node('Cookie', headers['Cookie'])
        response.add_node('Data', user_data)
        return response
