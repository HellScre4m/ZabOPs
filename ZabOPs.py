version = 0.1

import sys
sys.path.append('py-zabbix/')
import pyzabbix
from pyzabbix import ZabbixAPI

import argparse
import cx_Oracle
import zabops_config

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
        if not check:
            printerr('No checks specified, exiting');
            return -1;
        self.args = parser.parse_args()

        if self.args.username is None:
            self.args.username = zabops_config.username
        if self.args.password is None:
            self.args.password = zabops_config.password
        if self.args.address is None:
            self.args.address = zabops_config.address
        if self.args.port is None:
            self.args.port = zabops_config.port

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

    def __call__(self):
        try:
            self.db_connect()
        except Exception, err:
            print
            str(err)
            return 1
        checks(self.args.check)
        self.db_close()
