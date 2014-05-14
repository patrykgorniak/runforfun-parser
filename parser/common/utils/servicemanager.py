import json
from parser.services.datasport import datasportmanager

servicesMgr = {}
servicesMgr['datasport'] = {
        'get_events': datasportmanager.get_events,
        'myaccount': datasportmanager.myaccount
}


def __error__(reason):
    return json.dumps({'Status': 'FAILED', 'Data': '{0} does not exist.'.format(reason)},
                      indent=4)


def run(service, action, args):
    if service in servicesMgr:
        if action in servicesMgr[service]:
            return servicesMgr[service][action](args)
        else:
            return __error__(action)
    else:
        return __error__(service)
