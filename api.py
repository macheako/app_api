#!/usr/bin/env python
# encoding: utf-8

import os
import pwd
import sys
import grp
import logging
import logging.handlers
import signal
import getopt
import time
import ConfigParser
import cherrypy

__version__   = '1.0'
__author__    = 'Matthew Morton'
__email__     = 'Macheako@gmail.com'

def usage():
    print 'Usage: get rekt'
    sys.exit(1)

def version():
    print 'Dis Shit: Some API Version %s ' % __version__
    print 'Written by: %s (%s)' % (__author__, __email__)
    sys.exit(1)

def signalHandler(signal, frame):
    logger.warning('Received SIGTERM: Attempting graceful shutdown')
    SMSGateway.listen_for_sms = False
    SMSGateway.error_checking = False
    cherrypy.engine.stop()
    cherrypy.engine.exit()

def main():
    # Configure signal handling
    signal.signal( signal.SIGTERM, signalHandler )

    # Define global logger
    global logger
    global config

    # Set default values
    proj_path   = os.path.dirname(os.path.realpath(__file__))
    config_file = proj_path + '/etc/api.conf'
    daemonize   = False
    isRunning   = True
    log_level   = 'INFO'
    log_levels  = { 'DEBUG'    : logging.DEBUG,
                    'INFO'     : logging.INFO,
                    'WARNING'  : logging.WARNING,
                    'ERROR'    : logging.ERROR,
                    'CRITICAL' : logging.CRITICAL }

    # Parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:l:dhv',
            [
                'config=',
                'loglvl=',
                'daemonize',
                'help',
                'version'
            ])

    except getopt.GetoptError, err:
        usage()
        sys.exit(1)

    for option, value in opts:
        if option in ('--help', '-h'):
            usage()
            sys.exit(1)

        if option in ('--version', '-v'):
            version()
            sys.exit(1)

        if option in ('--loglvl', '-l'):
            log_level = value.upper()

        if option in ('--daemonize', '-d'):
            daemonize = True

        if option in ('--config', '-c'):
            config_file = value

    # Create configuration file object and parse the contents
    try:
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
    except ConfigParser.Error as e:
        print e.__str__()
        sys.exit(1)

    # Set up logging
    logger    = logging.getLogger('__main__')
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%b %d %H:%M:%S')
    handler   = logging.handlers.RotatingFileHandler( filename=config.get('main', 'log_file'),
                                                    mode='a',
                                                    maxBytes=4194304,
                                                    backupCount=4 )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Check correct log level was passed
    if log_level not in log_levels:
        print "Error: Invalid log level supplied. Falling back to default level: INFO"
        print "Usable values include: DEBUG, INFO, WARNING, ERROR, CRITICAL"
        log_level = 'INFO'
    else:
        logger.setLevel(log_levels[log_level])

    apiserver = RESTful(config)
    apiserver.start()

if __name__ == '__main__':
    from modules.rest import RESTful

    try:
        main()
    except KeyboardInterrupt:
        pid = os.getpid()
        os.kill(pid, signal.SIGTERM)
