import json
from services.datasport import datasportmanager

servicesMgr = {}

servicesMgr['datasport'] = {
    'get_events': datasportmanager.get_events
}


def __error__(reason):
    return json.dumps({'Status': 'Error', 'Data': '{} does not exist.'.format(reason)},
                      indent=4)


def run(service, action, args):
    if service in servicesMgr:
        if action in servicesMgr[service]:
            return servicesMgr[service][action]()
        else:
            return __error__(action)
    else:
        return __error__(service)
