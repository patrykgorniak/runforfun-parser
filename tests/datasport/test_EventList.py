#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_EventList
----------------------------------

Tests for `EventList` functionality.
"""


import unittest
from parser.services.datasport import EventList


class TestEventList(unittest.TestCase):

    def setUp(self):
        self.args = {}
        self.args['url'] = "file:./data/EventLists.html"
        self.items = EventList.get_events_list(None, self.args)

    def test_events_list_count(self):
        self.assertEqual(len(self.items), 1066, "Incorrect size of events")

    def test_event_list_check_elements(self):
        self.assertEqual(self.items[0]['location'], "Legnica")
        self.assertEqual(self.items[0]['type'], EventList.EventType.RUNNING)
        self.assertEqual(self.items[0]['results_page'], "")
        self.assertEqual(self.items[0]['website'], "")
        self.assertEqual(self.items[0]['name'], "LEGNICA PÓŁMARATON - XXVII Bieg Lwa Legnickiego")
        self.assertEqual(self.items[0]['date'], "2014-10-12")

    def test_get_event_type_from_string(self):
        self.assertEqual(self.items[0]['location'], "Legnica")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
