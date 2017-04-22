from Src.SqliteMultithread import DataBase, DataTypeBase, data_type_decorator

__metaclass__ = type


@data_type_decorator
class License(DataTypeBase):
    data_base = DataBase(
        ["department_sid", "application_sid",
         "license_sid", "type", "text"],
        {
            "department_sid": 0,
            "application_sid": 0,

            "license_sid": 0,
            "type": "",
            "text": ""
        }
    )
