from parser.services.datasport import eventlist
from parser.services.datasport.urls import COMMON_DATA
from parser.common.utils import httpmanager
import urllib
import logging
logger = logging.getLogger("EventList")
import json


def get_events(filter=None):
    args = {}
    res, content = httpmanager.httprequest(COMMON_DATA['EVENT_LIST']['URL'], COMMON_DATA['LOGIN']['LOGIN_NEEDED'], args)
    results = eventlist.unpack_events(content, args)
    return json.dumps({'Status': 'OK', 'Data': results}, indent=4)


def login(args=None):
    args = {'login': 'Patryk.Gorniak', 'haslo': 'dupa1234'}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    res, cont = httpmanager.httprequest(COMMON_DATA['LOGIN']['URL'], COMMON_DATA['LOGIN']['LOGIN_NEEDED'], args, 'POST', headers, urllib.parse.urlencode(args))
    return (res['set-cookie'])
