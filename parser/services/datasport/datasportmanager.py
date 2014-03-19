from services.datasport import eventlist
from services.datasport.urls import COMMON_DATA
from common.utils import httpmanager
import logging
logger = logging.getLogger("EventList")
import json

def get_events(pattern=None):
    args={}
    content = httpmanager.httprequest(COMMON_DATA['EVENT_LIST']['URL'], args)
    results = eventlist.get_events_list(content, args)
    return json.dumps({ 'Status': 'OK', 'Data': results }, indent=4, ensure_ascii=False)
