import json
from parser.services.datasport import datasportmanager
from parser.common.utils.httpresponse import HttpResponse

servicesMgr = {}
servicesMgr['datasport'] = {
        'get_events': datasportmanager.get_events,
        'myaccount': datasportmanager.myaccount
}


def run(service, action, args):
    if service in servicesMgr:
        if action in servicesMgr[service]:
            obj = servicesMgr[service][action](args)
            if isinstance(obj, HttpResponse):
                return obj
            else:
                return HttpResponse.error("dupa")
        else:
            return HttpResponse.error(action)
    else:
        return HttpResponse.error(service)
