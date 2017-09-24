#!/usr/bin/env python
# encoding: utf-8

import sys
import cherrypy
import threading
import time
import logging
import ipaddr

from modules.login import Login

class RESTful(object):
    def __init__(self, config=None):
        self.logger = logging.getLogger('main.' + self.__class__.__name__)
        p = cherrypy.process.plugins.PIDFile(cherrypy.engine, config.get('main', 'pid_file'))
        p.subscribe()

        # Create the configuration for cherrypy
        cherrypy.tree.mount(
                Login(), '/login',
                {'/':
                    {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
                }
        )
        cherrypy_conf = {
            'server.socket_host' : '0.0.0.0',
            'server.socket_port' : 80,
            'server.thread_pool' : 10,

            # 'log.screen' : False,
            # 'log.error_file' : '/opt/app_api/logs/cherrypy_error.log',
            # 'log.access_file' : '/opt/app_api/logs/cherrypy.log'
        }

        cherrypy.config.update(cherrypy_conf)
        # cherrypy.tools.secret_filter = cherrypy.Tool('before_handler', self.secretFilter, priority=45)


    def start(self):
        cherrypy.engine.start()
        cherrypy.engine.block()

    def exit(self):
        cherrypy.engine.stop()
        cherrypy.engine.exit()
