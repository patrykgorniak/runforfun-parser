import json
from parser.services.datasport import datasportmanager
from parser.common.utils.httpresponse import *

servicesMgr = {}
servicesMgr['datasport'] = {
        'get_events': datasportmanager.get_events,
        'myaccount': datasportmanager.myaccount,
        'get_user_events': datasportmanager.get_user_events
}


def run(service, action, args):
    if service in servicesMgr:
        if action in servicesMgr[service]:
            obj = servicesMgr[service][action](args)
            if isinstance(obj, HttpResponse):
                return obj
            else:
                return HttpResponse()
        else:
            return __error__(action)
    else:
        return __error__(service)


def __error__(reason):
    resp = HttpResponse()
    resp.add_node("Data", "Missing {} section".format(reason))
    return resp
