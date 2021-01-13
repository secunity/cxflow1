

LOG_INIT = '__log_init__'


NAME = 'secunity-cxflow1'


cnf = {
    LOG_INIT: False,
    'name': NAME,
}

SECUNITY_FOLDER = '/etc/secunity'
__NFACCTD_SUPERVISOR_TASK_NAME__ = 'nfacctd'
__DEFAULT_CONF__ = 'secunity-cxflow.conf'


def get_args_parser():
    import argparse

    parser = argparse.ArgumentParser(description='Secunity Network Device XFlow Filter')
    parser.add_argument('-c', '--config', type=str, help='Config file (overriding all other options)', default=None)

    parser.add_argument('-l', '--logfile', type=str, help='File to log to', default=None)
    parser.add_argument('-v', '--verbose', type=bool, help='Indicates whether to log verbose data', default=False)

    parser.add_argument('--to_stdout', '--stdout', type=str, help='Log messages to stdout', default=False)
    parser.add_argument('--to_stderr', '--stderr', type=str, help='Log errors to stderr', default=False)

    parser.add_argument('-p', '--port', type=str, help='Listening port (UDP)', default=None)
    parser.add_argument('--identifier', '--id', type=str, help='Agent ID - must be XFlow Agent ID', default=None)
    parser.add_argument('-t', '--type', type=str, help='XFlow type (netflow/sflow/ipfix)', default=None)

    return parser