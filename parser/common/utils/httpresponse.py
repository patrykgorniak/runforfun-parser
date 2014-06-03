import json

class HttpResponse:
    def __init__(self):
       self.indent = 4
       self.container = {}

    def add_node(self, key, value):
        self.container[key] = value

    def __str__(self):
        return json.dumps(self.container, indent = self.indent)

    @staticmethod
    def error():
        return json.dumps({'Status': "FAILED"}, indent = 4)

    @staticmethod
    def error(reason):
        return json.dumps({'Status': "FAILED",  'Data': '{0} does not exist.'.format(reason)}, indent = 4)
