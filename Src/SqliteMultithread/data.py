import copy

__metaclass__ = type


class DataBase:
    def __init__(self, _key_lis, _dic_pro):
        self.key_lis = _key_lis
        self.dic_pro = _dic_pro
        self.key_or = {}
        self.table_cols = ""
        i = 0
        for key in self.key_lis:
            self.key_or[key] = i
            i += 1
            type_str = str(type(self.dic_pro[key]))
            if type_str == "<class 'str'>":
                self.table_cols += ("%s text, " % key)
            elif type_str == "<class 'datetime.date'>":
                self.table_cols += ("%s date, " % key)
            elif type_str == "<class 'datetime.datetime'>":
                self.table_cols += ("%s datetime, " % key)
            else:
                self.table_cols += ("%s int, " % key)
        self.table_cols = self.table_cols[:-2]


class DataTypeBase:
    def get_list(self):
        pass

    def get_tuple(self):
        pass

    def get_dict(self):
        pass

    def get_format(self):
        pass

    def get_update_format(self):
        pass

    @staticmethod
    def get_table_col():
        pass


def data_type_decorator(data_type_base):
    class DataType:
        data_base = data_type_base.data_base

        def __init__(self, arg):
            arg_type = str(type(arg))
            self.dic = copy.deepcopy(data_type_base.data_base.dic_pro)
            if arg_type == "<class 'dict'>":
                self.dic.update(arg)
            elif arg_type == "<class 'list'>" or arg_type == "<class 'tuple'>":
                for key in data_type_base.data_base.key_lis:
                    self.dic[key] = arg[data_type_base.data_base.key_or[key]]
            self.formats = ""
            self.update_formats = ""
            for key in data_type_base.data_base.key_lis:
                type_str = str(type(self.dic[key]))
                if type_str == "<class 'str'>" or type_str == "<class 'datetime.date'>" \
                        or type_str == "<class 'datetime.datetime'>":
                    self.formats += ("'%s', " % self.dic[key])
                    self.update_formats += ("%s='%s', " % (key, self.dic[key]))
                else:
                    self.formats += str(self.dic[key]) + ", "
                    self.update_formats += ("%s=%d, " % (key, self.dic[key]))
            self.formats = self.formats[:-2]
            self.update_formats = self.update_formats[:-2]

        def get_list(self):
            ret = []
            for key in data_type_base.data_base.key_lis:
                ret.append(self.dic[key])
            return ret

        def get_tuple(self):
            return tuple(self.get_list())

        def get_dict(self):
            return self.dic

        def get_format(self):
            return self.formats

        def get_update_format(self):
            return self.update_formats

        @staticmethod
        def get_table_col():
            return data_type_base.data_base.table_cols

    return DataType
