from parser.services.datasport import eventlist
from parser.services.datasport.urls import COMMON_DATA
from parser.common.utils import httpmanager
from parser.services.datasport import authorization
from parser.services.datasport import accountmanager
import urllib
import logging
import json
logger = logging.getLogger(__name__)


def get_events(args=None):
    args = {}
    res, content = httpmanager.httprequest(COMMON_DATA['EVENT_LIST']['URL'], COMMON_DATA['LOGIN']['LOGIN_NEEDED'], args)
    results = eventlist.unpack_events(content, args)
    return json.dumps({'Status': res.reason, 'Data': results}, indent=4)


def login(args=None):
    args = {'login': 'Patryk.Gorniak', 'haslo': 'dupa1234'}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    res, cont = httpmanager.httprequest(COMMON_DATA['LOGIN']['URL'], COMMON_DATA['LOGIN']['LOGIN_NEEDED'], args, 'POST', headers, urllib.parse.urlencode(args))
#    headers = {}
#    headers['Cookie'] = res['set-cookie']
#    res, cont = httpmanager.httprequest(COMMON_DATA['USER_DATA']['URL'], COMMON_DATA['USER_DATA']['LOGIN_NEEDED'], args, 'GET', headers)
    return (res['set-cookie'])

def myaccount(args):
    headers = authorization.checkCredentials(args)
    if headers['Cookie']=="":
        return json.dumps( {'Status': "FAILED", 'Cookie':""}, indent = 4)
    else:
        params = {'id': '1413', 'los': '2015'}
        res, cont = httpmanager.httprequest(COMMON_DATA['CHANGE_USER_DATA']['URL'], COMMON_DATA['CHANGE_USER_DATA']['LOGIN_NEEDED'], params, 'GET', headers)
        text = cont.decode('cp1250')
        print(text)
        if text.find('Wyloguj mnie') > -1:
            results = accountmanager.get_user_data(text)
            return json.dumps({'Status':res.reason, 'Cookie':"", 'Data':results }, indent = 4)
        else:
            return json.dumps( {'Status': "FAILED", 'Cookie':""}, indent = 4)
