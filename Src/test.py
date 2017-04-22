from Src.datas import Process
import datetime

p = Process([
    "材料审查", 1, 1,
    "是否通过,int,bool_box;审查意见,text,text_area"])
q = Process([
    "材料受理", 2, 2,
    "是否通过,int,bool_box;受理意见,text,text_area"])

print(p.get_form_dict())
print(p.get_form_format())

print(p.get_form_update_format({
    "application_sid": 1,
    "order_in_application": 2,
    "user_sid": 4,
    "dispose_time": datetime.datetime.now(),
    "data0": 1,
    "data1": "你好"
}))
