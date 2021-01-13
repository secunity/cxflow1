#!/usr/bin/env python3

"""
All rights reserved to Secunity 2021
"""
import collections
import datetime
import os
import re
import shlex
import subprocess
from ipaddress import IPv4Network, IPv4Address
from conf import SECUNITY_FOLDER, __DEFAULT_CONF__, __NFACCTD_SUPERVISOR_TASK_NAME__
import requests
from logger import log


_URL = {
    'url_host': 'api.secunity.io',
    'url_scheme': 'https',
    'url_path': 'cxflow1/v1.0.0/in/account/{identifier}/{protocol}/',
    'url_method': 'GET'
}

MAX_PORT = 65535


_DEFAULTS = {
    'tag': 100,
    'interval': '1h',
    'protocol': 'netflow',

    'nfacctd_config': 'nfacctd.conf',
    'networks_config': 'secunity-networks.map',
    'forwarders': 'secunity-forwarders.lst'
}

_scheduler = None


def _parse_identifier(identifier=None, **kwargs):
    if not identifier:
        identifier = kwargs.get('device_identifier') or kwargs.get('device') or kwargs.get('key')
    return identifier


def _make_request(**kwargs):
    empty = (None, None, None)
    identifier = _parse_identifier(**kwargs)
    if not identifier:
        error = f'invalid device identifier: {str(identifier or "")}'
        log.error(error)
        return empty

    con_params = {k: v for k, v in kwargs.items() if k == 'url' or k.startswith('url_')}
    if not con_params:
        log.exception('invalid connection params')
        return empty

    url = kwargs.get('url', con_params.get('url'))
    if not url:
        url_path = kwargs.get('url_path', con_params.get('url_path'))
        if '{' in url_path:
            kwargs['url_path'] = url_path.format(identifier=identifier, protocol=kwargs['protocol'])
        url_params = {
            _: kwargs.get(_, con_params.get(_))
            for _ in list(set(list(kwargs.keys()) + list(con_params.keys())))
            if _ == 'url' or _.startswith('url_')
        }

        url_port = url_params.get('url_port')
        if url_port:
            url_params['url_host'] = f"{url_params['url_host']}:{url_port}"
        url = '{url_scheme}://{url_host}/{url_path}'.format(**url_params)
        con_params.update(url_params)

    log.debug(f'making request for identifier {identifier} to {url}')
    try:
        res = requests.get(url)
        result = res.json()
    except Exception as ex:
        log.exception(f'failed to make request for identifier {identifier} to {url}: {str(ex)})')
        return empty

    if not result or not result.get('status'):
        log.warning('could not retrieve networks list - quiting')
        return empty

    data = result['data']
    collector = data['collector'].split(':')
    return collector[0], int(collector[1]), data['networks']


_is_int_lst_ = (True, False,)

def is_int(i):
    return isinstance(i, int) and i not in _is_int_lst_


def is_network(network):
    try:
        IPv4Network(network)
        return True
    except:
        return False


def is_ipv4(ip):
    try:
        IPv4Address(ip)
        return True
    except:
        return False


_network_line_regex = re.compile(r'^set_tag=(?P<tag>[0-9]+)\s+dst_net=(?P<network>[^\s]+)$')

def _get_current_networks(**kwargs):
    networks_file = os.path.join(SECUNITY_FOLDER, _DEFAULTS['networks_config'])
    if os.path.isfile(networks_file):
        with open(networks_file, 'r') as f:
            content = f.read()
        content = content.split('\n')
        content = [_.strip() for _ in content if _.strip() and not _.strip().startswith(';')]
        content = [_network_line_regex.match(_).groupdict() for _ in content]

        tag = content[0]['tag'] if content else _DEFAULTS['tag']
        networks = [_['network'] for _ in content]
    else:
        tag = _DEFAULTS['tag']
        networks = []

    return tag, networks

def _get_current_forwarders(tag=None, **kwargs):
    if not tag:
        tag = _DEFAULTS['tag']
    forwarders_file = os.path.join(SECUNITY_FOLDER, _DEFAULTS['forwarders'])
    if os.path.isfile(forwarders_file):
        with open(forwarders_file, 'r') as f:
            content = f.read()
        content = content.split('\n')
        content = [_.strip() for _ in content if _.strip() and not _.strip().startswith(';')]
        forwarders_line_regex = re.compile(rf'^id=[0-9]+\s+ip=([^\s]+)\s+tag={tag}$')

        forwarders = [forwarders_line_regex.match(_).groups()[0] for _ in content]
        return forwarders
    else:
        return []


def _write_files(port, networks, forwarders, tag=None, **kwargs):
    if not tag:
        tag = _DEFAULTS['tag']

    networks_file = os.path.join(SECUNITY_FOLDER, _DEFAULTS['networks_config'])
    forwarders_file = os.path.join(SECUNITY_FOLDER, _DEFAULTS['forwarders'])

    def _write_networks_file():
        lines = [f'set_tag={tag} dst_net={_}' for _ in networks]
        lines = '\n'.join(lines)
        with open(networks_file, 'w') as f:
            f.write(lines)

    def _write_forwarders_file():
        lines = [f'id={i+1}   ip={_}    tag={tag}' for i, _ in enumerate(forwarders)]
        lines = '\n'.join(lines)
        with open(forwarders_file, 'w') as f:
            f.write(lines)

    def _write_nfacctd():
        nfacctd_file = os.path.join(SECUNITY_FOLDER, _DEFAULTS['nfacctd_config'])
        lines = [
            # 'daemonize: true',
            f'nfacctd_port: {port}',

            'plugins: tee[a]',
            f'tee_receivers[a]: {forwarders_file}',
            f'pre_tag_map[a]: {networks_file}'
        ]
        lines = '\n'.join(lines)
        with open(nfacctd_file, 'w') as f:
            f.write(lines)

    _write_networks_file()
    _write_forwarders_file()
    _write_nfacctd()


def _diff_lists(list1, list2):
    if list1 is None:
        list1 = []
    if list2 is None:
        list2 = []
    return collections.Counter(list1) != collections.Counter(list2)


def restart_supervisor_tasks():
    command = f'supervisorctl restart {__NFACCTD_SUPERVISOR_TASK_NAME__}'
    try:
        log.debug(f'restarting {__NFACCTD_SUPERVISOR_TASK_NAME__} service')
        res = subprocess.check_output(shlex.split(command))
        log.debug(f'result: {res}')
    except Exception as ex:
        log.exception(f'failed to restart {__NFACCTD_SUPERVISOR_TASK_NAME__} task: "{str(ex)}"')
        return False

    return True


def _work(**kwargs):
    log.debug('starting iteration')

    collector_ip, collector_port, networks = _make_request(**kwargs)
    if not is_ipv4(collector_ip) or not collector_port or collector_port <= 0:
        log.error('invalid or no collector was specified - quiting')
        return False

    if not networks:
        log.warning('empty list of networks')
        networks = []

    collector = f'{collector_ip}:{collector_port}'
    tag, cur_networks = _get_current_networks(**kwargs)

    networks_diff = _diff_lists(cur_networks, networks)

    if not networks_diff: # and not collector_diff:
        log.debug('no networks changes - quiting')
        return

    # full_forwarders = list(set(kwargs.get('forwarders', []) + [collector]))
    log.debug('rewriting filter config files')
    _write_files(port=kwargs['port'], networks=networks, forwarders=[collector])
    log.debug('filter config files has been rewritten')

    log.debug('restarting supervisord tasks')
    restart_supervisor_tasks()
    log.debug('supervisord tasks restarted')

    log.debug(f'finished iteration')


def _start_scheduler(**kwargs):
    from apscheduler.triggers.interval import IntervalTrigger
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.executors.pool import ThreadPoolExecutor
    import pytz

    log.debug('initializing scheduler and jobs')
    global _scheduler
    _scheduler = BackgroundScheduler(executors={'default': ThreadPoolExecutor(30)},
                                     job_defaults={'max_instances': 1},
                                     timezone=pytz.utc)

    _scheduler.add_job(func=_work,
                       trigger=IntervalTrigger(seconds=args['interval'].total_seconds()),
                       kwargs=kwargs,
                       max_instances=1,
                       next_run_time=datetime.datetime.utcnow() + datetime.timedelta(seconds=1))

    _scheduler.start()
    log.debug('scheduler and jobs initialized')


def _parse_config(config, **kwargs):
    if not os.path.isfile(config):
        log.error(f'missing config file: {config}')
        raise ValueError(f'missing config file: {config}')

    try:
        # allow remarks in config
        import jstyleson as json
    except:
        import json
    with open(config, 'r') as f:
        return json.load(f)


_re_interval = {
    'minute': re.compile(r'^\s*([1-9][0-9]*)\s*m\s*$', re.IGNORECASE),
    'hours': re.compile(r'^\s*([1-9][0-9]*)\s*h\s*$', re.IGNORECASE),
    'days': re.compile(r'^\s*([1-9][0-9]*)\s*d\s*$', re.IGNORECASE),
}

def _validate_args(args):
    identifier = args.get('identifier')
    if not identifier:
        log.error('identifier was not specified')
        return False
    try:
        from bson import ObjectId
        identifier = str(ObjectId(identifier))
    except:
        log.error(f'invalid identifier: "{identifier}"')
        return False

    port = args.get('port')
    if not port:
        log.error('listening port was not specified')
        return False
    if isinstance(port, str):
        port = args['port'] = int(port)
    if not is_int(port) or port <= 0 or port > MAX_PORT:
        log.error(f'invalid listening port: "{port}"')
        return False

    interval = args.get('interval')
    if not interval:
        interval = _DEFAULTS['interval']
    m = _re_interval['minute'].match(interval)
    if m:
        interval = datetime.timedelta(minutes=int(m.groups()[0]))
    else:
        m = _re_interval['hours'].match(interval)
        if m:
            interval = datetime.timedelta(hours=int(m.groups()[0]))
        elif _re_interval['days'].match(interval):
            interval = datetime.timedelta(days=int(m.groups()[0]))
        else:
            log.error(f'invalid interval: "{interval}"')
            return False
    args['interval'] = interval

    protocol = args.get('protocol', '').strip()
    if protocol:
        if protocol.lower() not in ('netflow', 'sflow', 'ipfix'):
            log.error(f'invalid protocol: "{protocol}"')
    else:
        protocol = _DEFAULTS['protocol']
    args['protocol'] = protocol.lower()

    return True


def _parse_enviroment_vars(args):
    for key in ('config', 'logfile', 'port', 'identifier', 'interval', 'protocol', 'url_scheme', 'url_host', 'url_port'):
        if args.get(key) is None:
            env_key = f'SECUNITY_{key.upper()}'
            args[key] = os.environ.get(env_key)
            if key in ('verbose', 'to_stdout', 'to_stderr', ) and not isinstance(args[key], bool):
                value = (args[key] or '').lower()
                args[key] = True if value == 'true' else \
                            False if value == 'false' else False
    return args

if __name__ == '__main__':
    import time
    import copy
    from conf import get_args_parser

    parser = get_args_parser()

    args = parser.parse_args()
    args = _parse_enviroment_vars(vars(args))

    _args = copy.deepcopy(_URL)
    _args.update({k: v for k, v in args.items() if v is not None})
    args = _args

    config = args.get('config')
    if not config:
        default_conf = os.path.join(SECUNITY_FOLDER, __DEFAULT_CONF__)
        if os.path.isfile(default_conf):
            config = args['config'] = default_conf
    if config:
        config = _parse_config(config)
        args.update(config)

    if _validate_args(args):
        _start_scheduler(**args)

    try:
        while True:
            time.sleep(1)
    except Exception as ex:
        log.warning(f'Stop signal recieved, shutting down scheduler: {str(ex)}')
        _scheduler.shutdown()
        log.warning('scheduler stopped')
        log.warning('quiting')










