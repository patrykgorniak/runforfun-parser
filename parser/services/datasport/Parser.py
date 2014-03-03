class DataSportParser():
    """DATA sport parser"""

###################################################################################
#------------------------------- Event Lists Section -----------------------------#
##################################################################################
    @staticmethod
    def parseEventList(HtmlEventsList):
        page_nr = 1
        page_size = 10
        offset = 0
        found = 0
        events = {}
        
        for htmlEvent in HtmlEventsList:
            if (offset / page_size) + 1 == page_nr and found < page_size:
                    parsed_row =  __parseeventlistrow(row)
                    event_id = offset + page_nr * page_size
                    events.update(event_id=parsed_row)
                    found += 1
            offset += 1
        return events


    def __parseeventlistrow(htmlEvent):
        # Get event type. For now it is image name f.g narty.gif, bieg.gif etc
        event_type_list = row[0].xpath(".//@src")
        event_type = EventType.OTHER if len(event_type_list) < 1 else get_event_type_from_string(row[0].xpath(".//@src")[0].replace('\n', '').strip().rstrip())
        event_date = row[0].xpath("string()").rstrip().strip()
        event_name = row[1][0].xpath("string()").rstrip().strip()
        location = row[2][0].xpath("string()").rstrip().strip()
        entry_list = row[3].xpath(".//@href")
        event_entries = "" if len(entry_list) < 1 else entry_list[0]
        result_page_list = row[4].xpath(".//@href")
        result_page = "" if len(result_page_list) < 1 else result_page_list[0]
        website_list = row[5].xpath(".//@href")
        website = "" if len(website_list) < 1 else website_list[0]
        
        info = EventInfo(event_type, event_name, location, event_date, event_entries, result_page, website)
        return vars(info)
