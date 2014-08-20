__author__ = 'dorbian'
__version__ = '1.0'

import os
import threading
import logging
from logging import handlers
import time

maxsize = 1000000
maxfiles = 5
logdir = "../Logs/"
loggername = "TraceLogger"
_debug = True
_verbose = True
filename = "log.txt"


class Loch(object):

    def __init__(self,filename, maxsize, maxfiles, logdir, loggername, level, _debug, _verbose):
        self.filename = filename
        self.maxsize = maxsize
        self.maxfiles = maxfiles
        self.logdir = os.path.abspath(logdir)
        self.loggername = loggername
        self.level = level
        self.logfilelocation = ""
        self._debug = _debug
        self._verbose = _verbose

    def initialize(self):

        logger = logging.getLogger(self.loggername)
        logger.setLevel(self.level)

        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)

        self.logfilelocation = os.path.join(self.logdir, self.filename)
        formatter = logging.Formatter('%(asctime)s - %(levelname)-7s :: %(message)s', '%d-%b-%Y %H:%M:%S')
        handler = handlers.RotatingFileHandler(self.logfilelocation, maxBytes=self.maxsize, backupCount=self.maxfiles, )
        handler.setLevel(self.level)

        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.INFO)
        if self._debug:
            streamhandler.setLevel(logging.DEBUG)
        streamhandler.setFormatter(formatter)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.addHandler(streamhandler)

    def log(self, msg, lvl):
        logger = logging.getLogger(self.loggername)
        thread = threading.currentThread().getName()

        #if self._verbose:
            #print("[{0}]-[{3}]::{2}::{1}".format(time.strftime("%Y-%m-%d %H:%M:%S"), msg, lvl, thread))

        msg = '[{0}]::{1}'.format(thread, msg)

        if lvl == 'DEBUG':
            logger.debug(msg)
        elif lvl == 'INFO':
            logger.info(msg)
        elif lvl == 'WARNING':
            logger.warn(msg)
        elif lvl == 'ERROR':
            logger.error(msg)
        else:
            logger.error("***UNKNOWN*** {0}".format(msg))

logwriter = Loch(filename, maxsize, maxfiles, logdir, loggername, logging.DEBUG, _debug, _verbose)
logwriter.initialize()

def log(message, level):
    if str(level).lower() == 'debug':
        logwriter.log(message, lvl='DEBUG')
    elif str(level).lower() == 'info':
        logwriter.log(message, lvl='INFO')
    elif str(level).lower() == 'warning':
        logwriter.log(message, lvl='WARNING')
    elif str(level).lower() == 'error':
        logwriter.log(message, lvl='ERROR')
    else:
        logwriter.log(message, lvl='')