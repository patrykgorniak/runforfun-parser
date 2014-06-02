from parser.services.datasport import eventlist
from parser.services.datasport.urls import COMMON_DATA
from parser.common.utils import httpmanager
from parser.services.datasport import authorization
from parser.services.datasport import accountmanager
import urllib
import logging
import json
logger = logging.getLogger("default")


def get_events(args=None):
    args = {}
    res, content = httpmanager.httprequest(COMMON_DATA['EVENT_LIST']['URL'], COMMON_DATA['LOGIN']['LOGIN_NEEDED'], args)
    results = eventlist.unpack_events(content, args)
    return json.dumps({'Status': res.reason, 'Data': results}, indent=4)


def myaccount(args):
    params = {}
    user_data = {}
    logger.debug("My account request.")
    ret, headers = authorization.login(args)

    if ret == -1:
        return json.dumps({'Status': "FAILED"}, indent=4)
    else:
        params['id'] = ret
        params['los'] = authorization.los()
        user_data['id'] = params['id']

        res, cont = httpmanager.httprequest(COMMON_DATA['CHANGE_USER_DATA']['URL'], COMMON_DATA['CHANGE_USER_DATA']['LOGIN_NEEDED'], params, 'GET', headers)
        user_data.update(accountmanager.get_user_data(cont))
        jsonf = json.dumps({'Status': res.reason, 'Cookie': headers['Cookie'], 'Data': user_data}, indent=4)
        return jsonf
