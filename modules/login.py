#!/usr/bin/env python
# encoding: utf-8

import json
import cherrypy
import logging

class Login(object):
    exposed = True

    def __init__(self):
        self.logger = logging.getLogger('__main__.' + self.__class__.__name__)

    @cherrypy.tools.json_out()
    def GET(self,msg_id=None):
        return { 'STATUS' : 'SUCCESS', 'RESPONSE' : 'GET' }

    @cherrypy.tools.json_out()
    def POST(self, number, msg):
        return { 'STATUS' : 'SUCCESS', 'RESPONSE' : 'POST' }

    @cherrypy.tools.json_out()
    def PUT(self, title=None):
        return { 'STATUS' : 'SUCCESS', 'RESPONSE' : 'PUT' }

    @cherrypy.tools.json_out()
    def DELETE(self):
        return { 'STATUS' : 'SUCCESS', 'RESPONSE' : 'DELETE' }
