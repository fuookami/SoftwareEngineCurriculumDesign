import datetime

from Src.SqliteMultithread import DataBase, DataTypeBase, data_type_decorator

__metaclass__ = type


@data_type_decorator
class Authority(DataTypeBase):
    data_base = DataBase(
        [
            "authority_name", "authority_sid", "processes"
        ],
        {
            "authority_name": "",
            "authority_sid": 0,
            "processes": ""
        }
    )


@data_type_decorator
class Department(DataTypeBase):
    data_base = DataBase(
        [
            "department_name", "department_sid", "businesses"
        ],
        {
            "department_name": "",
            "department_sid": 0,
            "businesses": ""
        }
    )


@data_type_decorator
class User(DataTypeBase):
    data_base = DataBase(
        [
            "account", "password", "user_sid", "department_sid", "authority_sid",
            "name", "tel", "mail", "entry_date"
        ],
        {
            "account": "",
            "password": "",
            "user_sid": 0,
            "department_sid": 0,
            "authority_sid": 0,
            "name": "",
            "tel": "",
            "mail": "",
            "entry_date": datetime.date.today()
        }
    )
