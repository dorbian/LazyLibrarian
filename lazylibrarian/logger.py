__author__ = 'dorbian'
__version__ = '1.0'

import os
import threading
import logging
from logging import handlers


class Loch(object):

    def __init__(self):
        self.filename = "lazylibrarian.log"
        self.maxsize = 1000000
        self.maxfiles = 5
        self.logdir = os.path.abspath("./Logs")
        self.loggername = __name__  # "TraceLogger"
        self.level = 9
        self.logfilelocation = ""
        self._debug = True
        self._trace = True

    def initialize(self):
        logging.addLevelName(9, "TRACE")
        logger = logging.getLogger(self.loggername)
        logger.setLevel(self.level)

        def trace(self, message, *args, **kws):
            self._log(9, message, args, **kws)
        logging.Logger.trace = trace

        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)

        self.logfilelocation = os.path.join(self.logdir, self.filename)
        formatter = logging.Formatter('%(asctime)s:[%(levelname)-5s]\t%(message)s', '%d-%b-%Y %H:%M:%S')
        handler = handlers.RotatingFileHandler(self.logfilelocation, maxBytes=self.maxsize, backupCount=self.maxfiles, )
        handler.setLevel(self.level)

        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.INFO)
        if self._debug:
            streamhandler.setLevel(10)
        if self._trace:
            streamhandler.setLevel(9)
        streamhandler.setFormatter(formatter)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.addHandler(streamhandler)

    def log(self, msg, lvl):

        logger = logging.getLogger(self.loggername)
        thread = threading.currentThread().getName()

        #if self._verbose:
            #print("[{0}]-[{3}]::{2}::{1}".format(time.strftime("%Y-%m-%d %H:%M:%S"), msg, lvl, thread))

        msg = '[{0}]\t{1}'.format(thread, msg)

        if lvl == 'DEBUG' and self._debug:
            logger.debug(msg)
        elif lvl == 'INFO':
            logger.info(msg)
        elif lvl == 'WARN':
            logger.warn(msg)
        elif lvl == 'ERROR':
            logger.error(msg)
        elif lvl == 'TRACE' and self._trace:
            logger.trace(msg)
        else:
            logger.error("***UNKNOWN*** {0}".format(msg))

logwriter = Loch()
logwriter.initialize()


#New format logging IMHO a better practice
def log(message, level):
    if str(level).lower() == 'debug':
        logwriter.log(message, lvl='DEBUG')
    elif str(level).lower() == 'info':
        logwriter.log(message, lvl='INFO')
    elif str(level).lower() == 'warning':
        logwriter.log(message, lvl='WARN')
    elif str(level).lower() == 'error':
        logwriter.log(message, lvl='ERROR')
    elif str(level).lower() == 'trace':
        logwriter.log(message, lvl='TRACE')
    else:
        logwriter.log(message, lvl='')


#Legacy Logging, will be moved over to new format
def debug(message):
    log(message, 'DEBUG')


def info(message):
    log(message, 'INFO')


def warn(message):
    log(message, 'WARNING')


def error(message):
    log(message, 'ERROR')