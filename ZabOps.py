version = 0.1

import sys
sys.path.append('py-zabbix/')
import pyzabbix
from pyzabbix import ZabbixAPI

import argparse
import json
import cx_Oracle

def printerr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


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
            '--port', help="Oracle database port")
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
        parser.add_argument(
            '--check', help="Check which agent wants to be done")
        self.args = parser.parse_args()
        with open('../config/zabps-config.json') as zabops_config:
            zabops_config = zabops_config.read()
        self.config = json.loads(zabops_config)
        if self.args.check is None
            #  log('No checks specified, exiting');
            sys.exit(0)
        if self.args.username is None:
            self.args.username = self.config.username
        if self.args.password is None:
            self.args.password = self.config.password
        if self.args.address is None:
            self.args.address = self.config.address
        if self.args.port is None:
            self.args.port = self.config.port

    def db_connect(self):
        dsn = cx_Oracle.makedsn(self.args.address, self.args.port,
                                self.args.database)
        self.pool = cx_Oracle.SessionPool(
            user=self.args.username,
            password=self.args.password,
            dsn=dsn,
            min=1,
            max=3,
            increment=1)
        self.db = self.pool.acquire()
        self.cur = self.db.cursor()

    def db_close(self):
        self.cur.close()
        self.pool.release(self.db)

    def checks(check):
        dba_config =
    def __call__(self):
        try:
            self.db_connect()
            checks(self.args.check)
        except Exception as err:
            # log(str(err))
            sys.exit(1)
        finally:
            self.db_close()



