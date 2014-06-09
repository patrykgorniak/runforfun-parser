import json
from enum import Enum

class HttpResponseStatus:
    FAILED = "FAILED"
    OK = "OK"

class HttpResponse:
    def __init__(self):
       self.indent = 4
       self.container = {"Status": HttpResponseStatus.FAILED }

    def set_status(self, value):
        self.container["Status"] = value

    def add_node(self, key, value):
        self.container[key] = value

    def __str__(self):
        return json.dumps(self.container, indent = self.indent)

#    @staticmethod
#    def error(*args):
#        if len(args) == 0:
#            return json.dumps({'Status': "FAILED"}, indent=4)
#        elif len(args) == 1:
#            return json.dumps({'Status': "FAILED",  'Data': '{0} does not exist!'.format(args[0])}, indent=4)
#        else:
#            pass
