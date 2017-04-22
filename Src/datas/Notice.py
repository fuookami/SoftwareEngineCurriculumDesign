import datetime

from Src.SqliteMultithread import DataBase, DataTypeBase, data_type_decorator

__metaclass__ = type


@data_type_decorator
class Notice(DataTypeBase):
    data_base = DataBase(
        ["notice_sid", "application_sid", "has_send",
         "title", "time", "sender", "text"],
        {
            "notice_sid": 0,
            "application_sid": 0,
            "has_send": 0,

            "title": "",
            "time": datetime.datetime.now(),
            "sender": "",
            "text": ""
        }
    )
