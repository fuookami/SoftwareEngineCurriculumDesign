from Src.SqliteMultithread.SqliteMultithread import SqliteMultithread
from Src.SqliteMultithread.data import *

db_url = r'D:\编程习题\其他\软工课设\work_flow_server_side\Src\SECD.sqlite3'
conn = SqliteMultithread(db_url, True, 'OFF')


def execute(req):
    conn.execute(req)


def select(req):
    ret = []
    for row in conn.select(req):
        ret.append(row)
    return ret
