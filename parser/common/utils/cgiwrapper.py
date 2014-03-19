STATUS_OK = 'Status: 200 OK'
STATUS_UNAUTHORIZED = 'Status: 403 Unauthorized'

CONTENT_HTML = "Content-type: text/html; charset=UTF-8"
CONTENT_PLAIN = "Content-type: text/plain; charset=UTF-8"
CONTENT_JSON = "Content-type: application/json;  charset=UTF-8"



def publish(content=None):
    if content is None:
        content = "Error occured!"

    print(STATUS_OK)
    print(CONTENT_PLAIN)
    print("Length: {}".format(len(content)))
    print()
    print(content)
