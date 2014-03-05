#!/usr/bin/env python
import cgi
import cgitb
from parser.services import datasport

import logging
import logging.config
from parser.common.utils import httpmanager
logging.config.fileConfig('common/configs/logger.conf')
logger = logging.getLogger(__name__)

default_action = 'events'
default_page_size = 10
default_page = 1
default_body = "You must specify action to perform"
args = {}
form = cgi.FieldStorage()
action = form.getvalue('action', default_action)
if action == "events":
    args['page_size'] = int(form.getvalue('page_size', default_page_size))
    args['page'] = int(form.getvalue('page', default_page))
    args['url'] = "http://online.datasport.pl/#kotw11"
    httpmanager.call_api_func(EventList.get_events_list, args, False)
elif action == 'login':
    args['user'] = form.getvalue("user", "")
    args['pass'] = form.getvalue("password", "")
    httpmanager.call_api_func(login, args, False)
elif action == 'logout':
    httpmanager.call_api_func(logout, args, True)
elif action == "change_password":
    args['old'] = form.getvalue("old", "")
    args['new'] = form.getvalue("new", "")
    httpmanager.call_api_func(change_password, args, True)
elif action == "get_user_data":
    httpmanager.call_api_func(get_user_data, {}, True)
elif action == "find_by_name":
    args['pattern'] = form.getvalue('pattern', "")
    httpmanager.call_api_func(Search.search_by_name, args, True)
else:
    print("Status: 200 OK")
    print("Content-type: text/html")
    print("Length: ", len(default_body))
    print("")
    print(default_body)
