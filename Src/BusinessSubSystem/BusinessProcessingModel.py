import json
import copy

from .Pub import application_info_cols, application_info_format

from Src import SqliteMultithread
from Src import DjangoHttpRequest
from Src.datas import User, Process, list_to_condition


def login(request):
    ret = {}
    data = json.loads(request.POST["data"])

    rows = SqliteMultithread.select("""SELECT * FROM User WHERE account='%s'"""
                                    % data["account"])
    if rows.__len__() != 0:
        for row in rows:
            user_dict = User(row).get_dict()
            if user_dict["password"] == data["password"]:
                ret["sta"] = 1
                ret.update(user_dict)
                ret.pop("password")
                break
        if ret.get("sta") is None:
            ret["sta"] = 0
    else:
        ret["sta"] = 2
    return DjangoHttpRequest.before_send_dispose(ret)


def get_application_info(request):
    ret = {
        "sta": 0,
        "application_info": []
    }
    data = json.loads(request.POST["data"])
    data["authority_sid"] = int(data["authority_sid"])
    data["department_sid"] = int(data["department_sid"])

    processes_sid_str = SqliteMultithread.select(
        """
        SELECT processes FROM Authority WHERE authority_sid = %d
        """ % data["authority_sid"]
    )[0][0].split(" ")
    processes_sid = []
    for process_sid_str in processes_sid_str:
        processes_sid.append(int(process_sid_str))

    businesses_sid_str = SqliteMultithread.select(
        """
        SELECT businesses FROM Department WHERE department_sid = %d
        """ % data["department_sid"]
    )[0][0].split(" ")
    businesses_sid = []
    for business_sid_str in businesses_sid_str:
        businesses_sid.append(int(business_sid_str))

    application_info_rows = SqliteMultithread.select(
        """
        SELECT %s FROM Application LEFT OUTER JOIN ApplicationContent AS Content
        ON Application.application_sid = Content.application_sid
        LEFT OUTER JOIN Business ON Application.business_sid = Business.business_sid
        LEFT OUTER JOIN Process AS CurrProcess ON Application.curr_process_sid = CurrProcess.process_sid
        WHERE (%s) AND (%s) ORDER BY Content.accept_final_time
        """ % (application_info_format, list_to_condition("Application.curr_process_sid", processes_sid, True),
               list_to_condition("Application.business_sid", businesses_sid, True))
    )

    if application_info_rows.__len__() >= 1:
        ret["sta"] = 1
        for application_info_row in application_info_rows:
            this_row = {}
            for i in range(0, application_info_cols.__len__()):
                this_row[application_info_cols[i]] = application_info_row[i]
            ret["application_info"].append(copy.deepcopy(this_row))
    else:
        ret.pop("application_info")

    return DjangoHttpRequest.before_send_dispose(ret)


def upload_form(request):
    data = json.loads(request.POST["data"])

    data["application_sid"] = int(data["application_sid"])
    data["order_in_application"] = int(data["order_in_application"]) + 1
    data["user_sid"] = int(data["user_sid"])
    curr_order = int(data["curr_order"])
    data.pop("curr_order")
    next_order = int(data["next_order"])
    data.pop("next_order")
    next_sid = int(data["next_sid"])
    data.pop("next_sid")
    process_sid = int(data["process_sid"])
    data.pop("process_sid")

    has_dispose_process_orders = SqliteMultithread.select(
        """
        SELECT has_dispose_process_orders FROM Application WHERE application_sid = %d
        """ % data["application_sid"]
    )[0][0]
    if has_dispose_process_orders == "":
        has_dispose_process_orders = " " + str(curr_order)
    else:
        has_dispose_process_orders += " " + str(curr_order)

    SqliteMultithread.execute(
        """
        UPDATE Application SET curr_process_sid = %d, curr_process_order = %d, has_dispose_process_orders = '%s'
        WHERE application_sid = %d
        """ % (next_sid, next_order, has_dispose_process_orders, data["application_sid"])
    )

    process = Process(SqliteMultithread.select(
        """
        SELECT * FROM Process WHERE process_sid = %d
        """ % process_sid
    )[0])

    SqliteMultithread.execute(
        """
        INSERT INTO ProcessForm%d VALUES (%s)
        """ % (process_sid, process.get_form_insert_format(data))
    )

    if next_order == 0:
        generate_license(data["application_sid"])
        generate_notice(data["application_sid"])

    return DjangoHttpRequest.before_send_dispose({})


def generate_license(application_sid):
    pass


def generate_notice(application_sid):
    pass


def send_notice(request):
    pass

