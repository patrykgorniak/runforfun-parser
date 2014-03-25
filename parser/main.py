#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import services.datasport.datasportmanager as datasport
from common.utils import cgiwrapper
from common.utils import httpmanager
from common.utils import servicemanager

import logging
import logging.config

form = cgi.FieldStorage()
default_action = 'login'
default_service = 'datasport'
service = form.getvalue('service', default_service)
action = form.getvalue('action', default_action)

cgiwrapper.publish(servicemanager.run(service, action, None))
