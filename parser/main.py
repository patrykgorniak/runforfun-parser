#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser.services.datasport.datasportmanager as datasport
from parser.common.utils import cgiwrapper
from parser.common.utils import httpmanager
from parser.common.utils import servicemanager
import os

import logging
import logging.config
BASEDIR=os.path.dirname(__file__)
logging.config.fileConfig(BASEDIR + '/common/configs/logger.conf')

def rff_run(request):
    if request.META['REQUEST_METHOD']=="GET":
        service = request.GET['service']
        action  = request.GET['action']
    else:
        service = request.GET['service']
        action  = request.GET['action']
    args = request.GET
    return servicemanager.run(service, action, args)

def run(_service, _action):
    cgiwrapper.publish(servicemanager.run(_service, _action, None))

if __name__ == '__main__':
    run(service, action)
