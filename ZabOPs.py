version = 0.1

import sys
sys.path.append('py-zabbix/')
import pyzabbix
from pyzabbix import ZabbixAPI

import argparse

class Main(Checks):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--address', required=True, help="Oracle database address")
        parser.add_argument(
            '--database', required=True, help="Oracle database SID")
        parser.add_argument('--username', help="Oracle database user")
        parser.add_argument(
            '--password', help="Oracle database user's password")
        parser.add_argument(
            '--port', default=1521, help="Oracle database port")
        parser.add_argument(
            '--ora1000',
            action='store_true',
            help="reconnect to Oracle database when request tablespace's size (bug 17897511)"
        )
        parser.add_argument(
            '--verbose',
            '-v',
            action='store_true',
            help="Additional verbose information")

        self.args = parser.parse_args()

        if self.args.username is None:
            self.args.username = zabops_config.username
        if self.args.password is None:
            self.args.password = zabops_config.password