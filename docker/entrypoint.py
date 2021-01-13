#!/usr/bin/env python
import os
import shlex
import subprocess
import sys

from conf import SECUNITY_FOLDER, __DEFAULT_CONF__
try:
    import jstyleson as json
except:
    import json
from conf import get_args_parser


_procs = {
    'supervisor': None,
}

def update_secunity_config(logger=None):
    parser = get_args_parser()
    args = parser.parse_args()
    args = {_: getattr(args, _) for _ in dir(args)
            if not _.startswith('_') and getattr(args, _) is not None}

    if args:
        file_name = os.path.join(SECUNITY_FOLDER, __DEFAULT_CONF__)
        if logger:
            logger.debug(f'changing conf file: "{file_name}"')
        if os.path.isfile(file_name):
            with open(file_name, 'r') as f:
                value = json.load(f)
        else:
            value = {}
        value.update(args)
        with open(file_name, 'w') as f:
            json.dump(value, f)
        if logger:
            logger.debug(f'conf file updated: "{file_name}"')
    else:
        logger.debug('no need to update config')

if __name__ == '__main__':
    import time
    import logging

    logger = logging.getLogger()
    logger.addHandler(sys.stdout)

    logger.debug('checking container switches')
    update_secunity_config(logger=logger)
    logger.debug('container switches handled')

    logger.debug('starting supervisord')
    _procs['supervisor'] = subprocess.Popen(shlex.split('supervisord -c /etc/supervisor/supervisord.conf'))
    logger.debug('supervisord started')

    while True:
        time.sleep(3)