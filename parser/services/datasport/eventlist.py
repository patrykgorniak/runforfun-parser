from pyquery import PyQuery
import logging
logger = logging.getLogger("EventList")


class EventType(object):
    RUNNING, CYCLING, SKIING, DOGS, BIATHLON, OTHER = range(0, 6)


def get_event_type_from_string(type):
    type_map = {
        'bieg.gif': EventType.RUNNING,
        'narty.gif': EventType.SKIING,
        'rower.gif': EventType.CYCLING,
        'pies.gif': EventType.DOGS,
        'biath.gif': EventType.BIATHLON,
    }
    return type_map.get(type, EventType.OTHER)


class EventInfo(object):
    name = ""
    type = EventType.OTHER
    location = ""
    date = ""
    entries = ""
    results_page = ""
    website = ""

    def __init__(self, type, name, location, date, entries, results_page, website):
        self.type = type
        self.name = name
        self.location = location
        self.date = date
        self.entries = entries
        self.results_page = results_page
        self.website = website

    def __str__(self):
        return "EventType: %d | EventName: %s | Location: %s | Date: %s | Entries: %s | Result Page: %s | Website: %s" % (self.type, self.name.encode('utf-8'), self.location.encode('utf-8'), self.date, self.entries, self.results_page, self.website.encode("utf-8"))



def __parse_row(entry_row):
    # Get event type. For now it is image name f.g narty.gif, bieg.gif et
    row = entry_row('td')
    event_type = get_event_type_from_string(row.find("img").attr("src"))
    event_date = row.find("font").eq(0).text()
    event_name = row.find("font").eq(1).text()
    location = row.find("font").eq(2).text()
    event_entries = "" if row.find("a").eq(0).attr("href") is None else row.find("a").eq(0).attr("href")
    result_page = "" if row.find("a").eq(1).attr("href") is None else row.find("a").eq(1).attr("href")
    website = "" if row.find("a").eq(2).attr("href") is None else row.find("a").eq(2).attr("href")
    info = EventInfo(event_type, event_name, location, event_date, event_entries, result_page, website)
    return vars(info)


def unpack_events(html, args):
    query = PyQuery(html)
    logger.debug("Source encoding: {} ".format(query.encoding))
    rows = query.items('tr')
    offset = 0
    events = {}
    for row in rows:
        parsed_row = __parse_row(row)
        event_id = offset
        events.update({event_id: parsed_row})
        offset += 1

    logger.debug("Parsed {} entries".format(offset))
    return events
