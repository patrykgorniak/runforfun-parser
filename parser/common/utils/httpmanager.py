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


httpHandler = httplib2.Http('.cache', disable_ssl_certificate_validation=True)

def httprequest(url, login_needed, args, method="GET", headers=None, body=None):
    params = ""

    for key, val in args.items():
        params +="&{0}={1}".format(key,val)
    logger.debug("Httprequest params: {0}".format(params))
    logger.debug("Httprequest headers: {0}".format(headers))
    logger.debug("Httprequest body: {0}".format(body))
    resp, content = httpHandler.request(url + '?' + params, method, headers=headers, body=body)
    return (resp, content.decode('cp1250'))
