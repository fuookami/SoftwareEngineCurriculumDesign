import json
import copy

from .Pub import application_info_cols, application_info_format

from Src import SqliteMultithread
from Src import DjangoHttpRequest

application_search_key_display = ["企业名称", "企业证件", "申请人联系方式", "联系人姓名", "联系人证件", "联系人联系方式"],
application_search_key = ["enterprise_name", "enterprise_certificate", "applicant_tel", "linkman_name",
                          "linkman_certificate", "linkman_tel"],


def get_search_keys(request):
    ret = {
        "sta": 1,
        "businesses_table": [],
        "application_search_key": application_search_key_display,
    }

    businesses_rows = SqliteMultithread.select(
        """
        SELECT business_sid, business_name FROM Business
        """
    )
    for row in businesses_rows:
        ret["businesses_table"].append({
            "business_sid": row[0],
            "business_name": row[1]
        })

    return DjangoHttpRequest.before_send_dispose(ret)


def search_get_application_info(request):
    ret = {
        "application_info": []
    }
    data = json.loads(request.POST["data"])
    data["key"] = int(data["key"])
    data["business_sid"] = int(data["business_sid"])

    if data["key"] < application_search_key.__len__():

        key = application_search_key[data["key"]]
        application_rows = []
        if key.find("certificate") == -1:
            application_rows = SqliteMultithread.select(
                """
                SELECT %s FROM Application LEFT OUTER JOIN ApplicationContent AS Content
                ON Application.application_sid = Content.application_sid
                LEFT OUTER JOIN Business ON Application.business_sid = Business.business_sid
                LEFT OUTER JOIN Process AS CurrProcess ON Application.curr_process_sid = CurrProcess.process_sid
                WHERE Application.business_sid = %d AND Content.%s = '%s'
                """ % (application_info_format, data["business_sid"], key, data["value"])
            )
        else:
            certificate = data["value"].split(" ")
            target = key.split("_")[0]
            application_rows = SqliteMultithread.select(
                """
                SELECT %s FROM Application FROM Application LEFT OUTER JOIN ApplicationContent AS Content
                ON Application.application_sid = Content.application_sid
                LEFT OUTER JOIN Business ON Application.business_sid = Business.business_sid
                LEFT OUTER JOIN Process AS CurrProcess ON Application.curr_process_sid = CurrProcess.process_sid
                WHERE Application.business_sid = %d
                AND Content.%s_certificate_type = '%s' AND Content.%s_certificate_id = '%s'
                """ % (application_info_format, data["business_sid"], target, certificate[0], target, certificate[1])
            )

        if application_rows.__len__() != 0:
            ret["sta"] = 1
            for application_row in application_rows:
                this_row = {}
                for i in range(0, application_info_cols.__len__()):
                    this_row[application_info_cols[i]] = application_row[i]
                ret["application_info"].append(copy.deepcopy(this_row))
        else:
            ret["sta"] = 0
    else:
        ret["sta"] = 2

    return DjangoHttpRequest.before_send_dispose(ret)
