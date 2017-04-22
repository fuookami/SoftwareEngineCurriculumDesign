from Src.SqliteMultithread import DataBase, DataTypeBase, data_type_decorator

__metaclass__ = type


def process_decorator(process_data_type):
    class ProcessDecorator(process_data_type):

        def __init__(self, arg):
            process_data_type.__init__(self, arg)
            self.__generate_dict_and_format()

        def get_form_format(self):
            return self.form_format

        def get_form_dict(self):
            return self.form_dict

        def get_form_update_format(self, arg):
            form_update_format = ""
            i = 0
            for form_dict in self.form_dict:
                if form_dict["label"] == "user_sid" or form_dict["label"] == "application_sid"\
                        or form_dict["label"] == "order_in_application":
                    form_update_format += form_dict["label"] + " = %d, " % arg[form_dict["label"]]
                elif form_dict["label"] == "dispose_time":
                    form_update_format += form_dict["label"] + " = datetime(CURRENT_TIMESTAMP, 'localtime'), "
                else:
                    if form_dict["label"] == "bool_box" or form_dict["label"] == "number":
                        form_update_format += "data" + str(i) + " = %d, " % int(arg["data" + str(i)])
                    elif form_dict["label"] == "text" or form_dict["label"] == "text_area" \
                            or form_dict["label"] == "datetime" or form_dict["label"] == "date":
                        form_update_format += "data" + str(i) + " = '%s', " % arg["data" + str(i)]
                    i += 1
            form_update_format = form_update_format[:-2]
            return form_update_format

        def get_form_insert_format(self, arg):
            form_insert_format = ""
            i = 0
            for form_dict in self.form_dict:
                if form_dict["label"] == "user_sid" or form_dict["label"] == "application_sid" \
                        or form_dict["label"] == "order_in_application":
                    form_insert_format += "%d, " % arg[form_dict["label"]]
                elif form_dict["label"] == "dispose_time":
                    form_insert_format += "datetime(CURRENT_TIMESTAMP, 'localtime'), "
                else:
                    if form_dict["label"] == "bool_box" or form_dict["label"] == "numbser":
                        form_insert_format += "%d, " % int(arg["data" + str(i)])
                    elif form_dict["label"] == "text" or form_dict["label"] == "text_area" \
                            or form_dict["label"] == "datetime" or form_dict["label"] == "date":
                        form_insert_format += "'%s', " % arg["data" + str(i)]
                    i += 1
            form_insert_format = form_insert_format[:-2]
            return form_insert_format

        def __generate_dict_and_format(self):
            self.form_format = "application_sid int, order_in_application int, " \
                               "user_sid int, dispose_time datetime, "
            self.form_dict = [{
                "name": "材料识别码",
                "type": "int",
                "label": "application_sid"
            }, {
                "name": "流程序号",
                "type": "int",
                "label": "order_in_application"
            }, {
                "name": "处理人用户识别码",
                "type": "int",
                "label": "user_sid"
            }, {
                "name": "处理时间",
                "type": "datetime",
                "label": "dispose_time"
            }]
            data = self.dic["form"].split(";")
            for i in range(0, data.__len__()):
                (name, type, label) = data[i].split(",")
                self.form_dict.append({
                    "name": name,
                    "type": type,
                    "label": label,
                })
                self.form_format += "data" + str(i) + " " + type + ", "
            self.form_format = self.form_format[:-2]

    return ProcessDecorator


@process_decorator
@data_type_decorator
class Process(DataTypeBase):
    data_base = DataBase(
        [
            "process_name", "process_sid", "dispose_authorities", "form"
        ],
        {
            "process_name": "",
            "process_sid": 0,
            "dispose_authorities": "",
            "form": ""
        }
    )


@data_type_decorator
class Business(DataTypeBase):
    data_base = DataBase(
        [
            "business_name", "business_sid", "dispose_departments", "processes"
        ],
        {
            "business_name": "",
            "business_sid": 0,
            "dispose_departments": "",
            "processes": ""
        }
    )
