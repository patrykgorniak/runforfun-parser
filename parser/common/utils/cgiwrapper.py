STATUS_OK = 'Status: 200 OK'
STATUS_UNAUTHORIZED = 'Status: 403 Unauthorized'

CONTENT_HTML = "Content-type: text/html"
CONTENT_PLAIN = "Content-type: text/plain"


def publish(content=None):
    if content is None:
        content = "Error occured!"

    print(STATUS_OK)
    print(CONTENT_HTML)
    print("Length: {}", len(content))
    print()
    print(content)
