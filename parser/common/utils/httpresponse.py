import json

class HttpResponse:
    def __init__(self):
       self.indent = 5
       self.container = {}

    def add_node(self, key, value):
        container[key] = value

    def error(self):
        return json.dumps({'Status': "FAILED"}, indent = self.indent)

    def __str__(self):
        return json.dumps(self.container, indent = self.indent)
