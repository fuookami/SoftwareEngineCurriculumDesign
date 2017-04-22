import sqlite3
from datetime import datetime
from Src.SqliteMultithread import db_url

from Src.datas import Process, Business, Authority, Department, User, Notice, License, Application, ApplicationContent


conn = sqlite3.connect(db_url)
cur = conn.cursor()
cur.execute("CREATE TABLE Process (%s)" % Process.get_table_col())
cur.execute("CREATE TABLE Business (%s)" % Business.get_table_col())
cur.execute("CREATE TABLE Authority (%s)" % Authority.get_table_col())
cur.execute("CREATE TABLE Department (%s)" % Department.get_table_col())
cur.execute("CREATE TABLE User (%s)" % User.get_table_col())
cur.execute("CREATE TABLE Notice (%s)" % Notice.get_table_col())
cur.execute("CREATE TABLE License (%s)" % License.get_table_col())
cur.execute("CREATE TABLE Application (%s)" % Application.get_table_col())
cur.execute("CREATE TABLE ApplicationContent (%s)" % ApplicationContent.get_table_col())
cur.execute("INSERT INTO User VALUES ('admin', 'admin', 0, 0, 0, '', '', '', '')")

default_application_content = \
    [
        (1, datetime(2016, 12, 14, 14, 0, 0), datetime(2016, 12, 21, 14, 0, 0),
        "申请者类型A", "企业A", "企业证件类型A", "1",
        "11111111111", "A市A区A路111号", "abc@def",
        "ABC", "身份证", "1", "22222222222", "B市B区B路222号", "333333", "ghi@jkl",
        "产品类型A", "A区", "", "", "", ""),
        (2, datetime(2016, 12, 15, 14, 0, 0), datetime(2016, 12, 22, 14, 0, 0),
        "申请者类型A", "企业B", "企业证件类型A", "2",
        "44444444444", "C市C区C路333号", "mno@pqr",
        "DEF", "身份证", "2", "55555555555", "D市D区D路444号", "666666", "stu@vwx",
        "产品类型A", "A区", "", "", "", ""),
        (3, datetime(2016, 12, 16, 14, 0, 0), datetime(2016, 12, 23, 14, 0, 0),
        "申请者类型B", "企业C", "企业证件类型B", "3",
        "77777777777", "E市E区E路555号", "yza@bcd",
        "HIJ", "护照", "3", "88888888888", "F市F区F路666号", "999999", "efg@hij",
        "产品类型A", "A区", "", "", "", ""),
        (4, datetime(2016, 12, 14, 14, 0, 0), datetime(2016, 12, 21, 14, 0, 0),
        "申请者类型A", "企业A", "企业证件类型A", "1",
        "11111111111", "A市A区A路111号", "klm@opq",
        "KLM", "身份证", "2", "11111111111", "B市C区C路233号", "223333", "rst@uvw",
        "产品类型A", "A区", "", "", "", ""),
        (5, datetime(2016, 12, 15, 14, 0, 0), datetime(2016, 12, 22, 14, 0, 0),
        "申请者类型B", "企业C", "企业证件类型B", "3",
        "77777777777", "E市E区E路555号", "yza@bcd",
        "HIJ", "护照", "3", "88888888888", "F市F区F路666号", "999999", "efg@hij",
        "产品类型A", "A区", "", "", "", ""),
        (6, datetime(2016, 12, 14, 14, 0, 0), datetime(2016, 12, 21, 14, 0, 0),
        "申请者类型A", "企业A", "企业证件类型A", "1",
        "11111111111", "A市A区A路111号", "abc@def",
        "ABC", "身份证", "1", "22222222222", "B市B区B路222号", "333333", "ghi@jkl",
        "产品类型A", "A区", "", "", "", ""),
        (7, datetime(2016, 12, 14, 14, 0, 0), datetime(2016, 12, 21, 14, 0, 0),
        "申请者类型A", "企业A", "企业证件类型A", "1",
        "11111111111", "A市A区A路111号", "abc@def",
        "ABC", "身份证", "1", "22222222222", "B市B区B路222号", "333333", "ghi@jkl",
        "产品类型A", "A区", "", "", "", ""),
        (8, datetime(2016, 12, 15, 14, 0, 0), datetime(2016, 12, 22, 14, 0, 0),
        "申请者类型A", "企业B", "企业证件类型A", "2",
        "44444444444", "C市C区C路333号", "mno@pqr",
        "DEF", "身份证", "2", "55555555555", "D市D区D路444号", "666666", "stu@vwx",
        "产品类型A", "A区", "", "", "", ""),
        (9, datetime(2016, 12, 14, 14, 0, 0), datetime(2016, 12, 21, 14, 0, 0),
        "申请者类型A", "企业A", "企业证件类型A", "1",
        "11111111111", "A市A区A路111号", "klm@opq",
        "KLM", "身份证", "2", "11111111111", "B市C区C路233号", "223333", "rst@uvw",
        "产品类型A", "A区", "", "", "", ""),
        (10, datetime(2016, 12, 14, 14, 0, 0), datetime(2016, 12, 21, 14, 0, 0),
        "申请者类型A", "企业A", "企业证件类型A", "1",
        "11111111111", "A市A区A路111号", "abc@def",
        "ABC", "身份证", "1", "22222222222", "B市B区B路222号", "333333", "ghi@jkl",
        "产品类型A", "A区", "", "", "", ""),
    ]

default_application = \
    [
        (1, 1, 1, 1, ""),
        (2, 1, 1, 1, ""),
        (3, 1, 1, 1, ""),
        (4, 1, 1, 1, ""),
        (5, 1, 1, 1, ""),
        (6, 1, 1, 1, ""),
        (7, 2, 1, 1, ""),
        (8, 2, 1, 1, ""),
        (9, 2, 1, 1, ""),
        (10, 2, 1, 1, ""),
    ]

for application in default_application_content:
    cur.execute("INSERT INTO ApplicationContent VALUES(%s)" % ApplicationContent(application).get_format())
for application in default_application:
    cur.execute("INSERT INTO Application VALUES(%s)" % Application(application).get_format())
conn.commit()
conn.close()
