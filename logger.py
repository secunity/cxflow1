import sys
import logging

from conf import cnf as _cnf, LOG_INIT, NAME


def _init_logger(logfile=None, verbose=False, to_stdout=False, to_stderr=False, **kwargs):
    logger = logging.getLogger(NAME)
    if _cnf[LOG_INIT]:
        return logger

    log_level = logging.DEBUG if verbose else logging.ERROR
    logger.setLevel(log_level)

    handlers = []
    if to_stdout:
        handlers.append(logging.StreamHandler(sys.stdout))
    if to_stderr:
        handlers.append(logging.StreamHandler(sys.stderr))
    if logfile:
        handlers.append(logging.FileHandler(logfile))

    for handler in handlers:
        handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if handlers:
        _cnf[LOG_INIT] = True
    return logger

class logMeta(type):

    def __getattr__(self, item):
        if item.upper() in self._methods:
            return getattr(self._log(), item.lower())

class log(metaclass=logMeta):

    _logger = None

    _methods = ('CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'EXCEPTION')

    @classmethod
    def _log(cls):
        if not cls._logger:
            cls._logger = _init_logger(**_cnf)
        return cls._logger