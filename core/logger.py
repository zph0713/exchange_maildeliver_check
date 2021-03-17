import os
from datetime import datetime
import logging
import time
from logging.handlers import RotatingFileHandler
import inspect




class Log(object):
    def __init__(self, name, console=1, logfile=None, show_details=False):
        self._level = logging.DEBUG
        self._mode = "a"
        self._max_bytes = 10 * 1024 * 1024
        self._rotate_count = 5
        self._log_file = logfile
        self._console = console
        self._lock_file = None
        self._fp = None

        self._logger = logging.getLogger(name)
        self._logger.setLevel(self._level)

        self._show_details = show_details

        logging.Formatter.converter = time.gmtime
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(threadName)s %(message)s")

        if self._console == 1:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self._logger.addHandler(stream_handler)

        if self._log_file is not None:
            self._lock_file = logfile + ".lock"

            rotate_handler = RotatingFileHandler(
                filename=self._log_file,
                mode=self._mode,
                maxBytes=self._max_bytes,
                backupCount=self._rotate_count)
            rotate_handler.setFormatter(formatter)
            self._logger.addHandler(rotate_handler)

    def set_debug_level(self):
        if self._logger is not None:
            self._logger.setLevel(logging.DEBUG)

    def set_info_level(self):
        if self._logger is not None:
            self._logger.setLevel(logging.INFO)

    def set_warning_level(self):
        if self._logger is not None:
            self._logger.setLevel(logging.WARNING)

    def set_error_level(self):
        if self._logger is not None:
            self._logger.setLevel(logging.ERROR)

    def set_critical_level(self):
        if self._logger is not None:
            self._logger.setLevel(logging.CRITICAL)

    def _lock(self):
        if self._lock_file is not None:
            self._fp = open(self._lock_file, 'w')
            if self._fp is not None:
                lock(self._fp, LOCK_EX)

    def _unlock(self):
        if self._fp is not None:
            unlock(self._fp)
            self._fp.close()

    def debug(self, msg, *args, **kwargs):
        if self._logger is not None:
            self._logger.debug(self.show_detail(msg), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self._logger is not None:
            self._logger.info(self.show_detail(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self._logger is not None:
            self._logger.warning(self.show_detail(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self._logger is not None:
            self._logger.error(self.show_detail(msg), *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self._logger is not None:
            self._logger.critical(self.show_detail(msg), *args, **kwargs)

    def show_detail(self, message):
        if not self._show_details:
            return message
        lastframe = inspect.currentframe().f_back.f_back
        funcName = lastframe.f_code.co_name
        filelineno = lastframe.f_lineno
        fileName = os.path.basename(lastframe.f_code.co_filename)
        return "%s (%s:%i)\t%s" % (
            funcName,
            fileName,
            filelineno,
            message)

def Logger(logname):
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    log_path = os.path.join(base_path, "logs")

    log_time = datetime.today().strftime('%Y-%m-%d')
    log_file = os.path.join(log_path, logname+"-" + str(log_time) + ".log")
    if not os.path.isdir(log_path):
        os.makedirs(log_path)

    logger_instance = Log(logname, console=1, logfile=log_file, show_details=True)
    return logger_instance

