import json
import copy

from Src import SqliteMultithread
from Src import DjangoHttpRequest
from Src.datas import Process, list_to_condition

application_info_cols = \
    ["application_sid", "business_name", "apply_time", "accept_final_time", "enterprise_name", "linkman_name",
     "product_type", "curr_process_name"]
application_info_format = ", ".join(
    ["Application.application_sid", "Business.business_name", "Content.apply_time", "Content.accept_final_time",
     "Content.enterprise_name", "Content.linkman_name", "Content.product_type", "CurrProcess.process_name"])

user_info_cols = \
    ["user_sid", "name", "department_name", "authority_name"]
user_info_format = ", ".join(
    ["User.user_sid", "User.name", "Department.department_name", 'Authority.authority_name'])


application_detail_cols = \
    ["application_sid", "business_name", "process_name", "apply_time", "accept_final_time", "applicant_type",
     "enterprise_name", "enterprise_certificate_type", "enterprise_certificate_id", "applicant_tel",
     "applicant_site", "applicant_mail", "linkman_name", "linkman_certificate_type", "linkman_certificate_id",
     "linkman_tel", "linkman_site", "linkman_postcode", "linkman_mail", "product_type", "enterprise_region"]
application_detail_format = ", ".join(
    ["Application.application_sid", "Business.business_name", "CurrProcess.process_name", "Content.apply_time",
     "Content.accept_final_time", "Content.applicant_type", "Content.enterprise_name",
     "Content.enterprise_certificate_type", "Content.enterprise_certificate_id", "Content.applicant_tel",
     "Content.applicant_site", "Content.applicant_mail", "Content.linkman_name", "Content.linkman_certificate_type",
     "Content.linkman_certificate_id", "Content.linkman_tel", "Content.linkman_site", "Content.linkman_postcode",
     "Content.linkman_mail", "Content.product_type", "Content.enterprise_region"])


def get_process_detail(request):
    data = json.loads(request.POST["data"])
    data["application_sid"] = int(data["application_sid"])

    ret = {
        "sta": 1,
        "application_detail": {},
        "dispose_info": {
            "processes_sid": [],  # in order
            "processes_info": [],
            "curr_process_order": 0,
            "has_dispose_process_orders": [],
            "forms": [],  # in order
            "next_process": {
                "over": "",
                "over_sid": 0,
                "not_over": "",
                "not_over_order": "",
            }
        }
    }

    application_detail_row = SqliteMultithread.select(
        """
        SELECT %s FROM Application LEFT OUTER JOIN ApplicationContent AS Content
        ON Application.application_sid = Content.application_sid
        LEFT OUTER JOIN Business ON Application.business_sid = Business.business_sid
        LEFT OUTER JOIN Process AS CurrProcess ON Application.curr_process_sid = CurrProcess.process_sid
        WHERE Application.application_sid = %d
        """ % (application_detail_format, data["application_sid"])
    )[0]
    for i in range(0, application_detail_cols.__len__()):
        ret["application_detail"].update({
            application_detail_cols[i]: application_detail_row[i]
        })

    (business_sid, curr_process_order, has_dispose_process_orders_str) = SqliteMultithread.select(
        """
        SELECT business_sid, curr_process_order, has_dispose_process_orders FROM Application WHERE application_sid = %d
        """ % data["application_sid"]
    )[0]

    has_dispose_process_orders = []
    if has_dispose_process_orders_str != "":
        has_dispose_process_orders_str = has_dispose_process_orders_str.split(" ")
        for has_dispose_process_order_str in has_dispose_process_orders_str:
            has_dispose_process_orders.append(int(has_dispose_process_order_str))
    ret["dispose_info"]["has_dispose_process_orders"] = has_dispose_process_orders
    curr_process_order = int(curr_process_order)
    ret["dispose_info"]["curr_process_order"] = curr_process_order

    this_business_processes_original_rows = SqliteMultithread.select(
        """
        SELECT processes FROM Business WHERE business_sid = %d
        """ % business_sid
    )[0][0].split(";")
    this_business_processes = []
    for this_business_processes_original_row in this_business_processes_original_rows:
        this_row = this_business_processes_original_row.split(",")
        if this_row[1] == "1":
            this_business_processes.append({
                "sid": int(this_row[0]),
                "not_over_go_next": True,
                "not_over_go_to_order": curr_process_order + 1
            })
        else:
            this_business_processes.append({
                "sid": int(this_row[0]),
                "not_over_go_next": False,
                "not_over_go_to_order": int(this_row[1][1:])
            })

    processes_sid = []
    for has_dispose_process_order in has_dispose_process_orders:
        processes_sid.append(this_business_processes[has_dispose_process_order - 1]["sid"])
    processes_sid.append(this_business_processes[curr_process_order - 1]["sid"])
    ret["dispose_info"]["processes_sid"] = copy.deepcopy(processes_sid)
    need_info_processes_sid = list(set(processes_sid))
    need_info_processes_sid.sort()

    over_next_process_sid = 0
    if curr_process_order == this_business_processes.__len__():
        over_next_process_sid = 0
    else:
        over_next_process_sid = this_business_processes[curr_process_order]["sid"]
    not_over_next_process_sid = 0
    if this_business_processes[curr_process_order - 1]["not_over_go_next"]:
        if curr_process_order == this_business_processes.__len__():
            not_over_next_process_sid = 0
        else:
            not_over_next_process_sid = this_business_processes[curr_process_order]["sid"]
    else:
        not_over_next_process_sid = this_business_processes[
            this_business_processes[curr_process_order - 1]["not_over_go_to_order"]]["sid"]
    processes_name_rows = SqliteMultithread.select(
        """
        SELECT process_name, process_sid FROM Process WHERE process_sid = %d OR process_sid = %d
        """ % (over_next_process_sid, not_over_next_process_sid)
    )
    for row in processes_name_rows:
        if int(row[1]) == over_next_process_sid:
            ret["dispose_info"]["next_process"]["over"] = row[0]
        else:
            ret["dispose_info"]["next_process"]["not_over"] = row[0]
    ret["dispose_info"]["next_process"]["over_sid"] = over_next_process_sid
    ret["dispose_info"]["next_process"]["not_over_order"] = \
        this_business_processes[curr_process_order - 1]["not_over_go_to_order"]

    processes_rows = SqliteMultithread.select(
        """
        SELECT * FROM Process WHERE (%s)
        """ % list_to_condition("process_sid", need_info_processes_sid, True)
    )
    for processes_row in processes_rows:
        process = Process(processes_row)
        process_dict = process.get_dict()
        ret["dispose_info"]["processes_info"].append({
            "process_sid": process_dict["process_sid"],
            "process_name": process_dict["process_name"],
            "form": process.get_form_dict()
        })

    users_info_rows = SqliteMultithread.select(
        """
        SELECT %s From User LEFT OUTER JOIN Department ON User.department_sid = Department.department_sid
        LEFT OUTER JOIN Authority ON User.authority_sid = Authority.authority_sid
        """ % user_info_format
    )
    users_info = {}
    for user_info_row in users_info_rows:
        users_info.update({
            int(user_info_row[0]): str(user_info_row[1]) + " (" + str(user_info_row[2]) + ", " + str(user_info_row[3]) + ")"
        })

    for i in range(1, processes_sid.__len__()):
        this_form = list(SqliteMultithread.select(
            """
            SELECT * FROM ProcessForm%d WHERE application_sid = %d AND order_in_application = %d
            """ % (processes_sid[i - 1], data["application_sid"], i)
        )[0])
        this_form[2] = users_info[int(this_form[2])]
        ret["dispose_info"]["forms"].append(copy.deepcopy(this_form))

    print(ret)
    return DjangoHttpRequest.before_send_dispose(ret)