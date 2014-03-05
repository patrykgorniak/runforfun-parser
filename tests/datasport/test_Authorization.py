#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_EventList
----------------------------------

Tests for `EventList` functionality.
"""


import unittest
from parser.services.datasport import authorization


class TestAuthorization(unittest.TestCase):
    response = None
    args = {}

    def setUp(self):
        self.args['user'] = "Patryk.Gorniak"
        self.args['pass'] = "dupa1234"

    def test_login(self):
        self.response = authorization.login(None, self.args)
        self.assertNotEqual(self.response, None)

    def test_logout(self):
        self.assertEqual(self.response, None)
        response = authorization.logout(self.response, self.args)
        self.assertEqual(response, None)

    def test_change_password(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
