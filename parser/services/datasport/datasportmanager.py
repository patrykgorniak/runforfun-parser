from services.datasport import eventlist
from services.datasport.urls import COMMON_DATA
from common.utils import httpmanager
import urllib
import logging
logger = logging.getLogger("EventList")
import json


def get_events(filter=None):
    args = {}
    res, content = httpmanager.httprequest(COMMON_DATA['EVENT_LIST']['URL'], COMMON_DATA['LOGIN']['login_needed'], args)
    results = eventlist.unpack_events(content, args)
    return json.dumps({'Status': 'OK', 'Data': results}, indent=4)


def login(filter=None):
    args = {'login': 'Patryk.Gorniak', 'haslo': 'dupa1234'}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    res, content = httpmanager.httprequest(COMMON_DATA['LOGIN']['URL'], COMMON_DATA['LOGIN']['login_needed'], args, 'POST', headers, urllib.parse.urlencode(args))
    return (res, content)
