import json
import copy
from Src import SqliteMultithread
from Src import DjangoHttpRequest
from Src.datas import Process, Business


def upload_process(request):
    data = json.loads(request.POST["data"])
    sid = SqliteMultithread.select("""SELECT COUNT(*) FROM Process""")[0][0] + 1

    form = ""
    form_dicts = data["form"]
    for form_dict in form_dicts:
        form += form_dict["name"] + "," + form_dict["type"] + "," + form_dict["label"] + ";"
    form = form[:-1]
    data.pop("form")

    dispose_authorities = " ".join(data["dispose_authorities"])
    authority_list = data["dispose_authorities"]
    for authority in authority_list:
        rows = SqliteMultithread.select(
            """
            SELECT processes FROM Authority WHERE authority_sid = %d
            """ % int(authority)
        )

        update_sql_sentences = ""
        for row in rows:
            processes = row[0]
            if processes == "":
                processes = str(sid)
            else:
                processes += " " + str(sid)
            update_sql_sentences += "UPDATE Authority SET processes = '%s' WHERE authority_sid = %d;" \
                                    % (processes, int(authority))
        update_sql_sentences = update_sql_sentences[:-1]
        SqliteMultithread.execute(update_sql_sentences)
    data.pop("dispose_authorities")

    data.update({
        "process_sid": sid,
        "dispose_authorities": dispose_authorities,
        "form": form
    })

    p = Process(data)
    SqliteMultithread.execute("""INSERT INTO Process VALUES(%s)""" % p.get_format())
    SqliteMultithread.execute("""CREATE TABLE ProcessForm%d (%s)""" % (sid, p.get_form_format()))
    return DjangoHttpRequest.before_send_dispose({})


def get_process(request):
    data = json.loads(request)
    data["process_sid"] = int(data["process_sid"])
    ret = {
        "sta": 1,
    }

    process_rows = SqliteMultithread.select(
        """
        SELECT * FROM process WHERE process_sid = %d
        """ % data["process_sid"]
    )

    if process_rows.__len__() == 1:
        process = Process(process_rows[0])
        ret["dispose_authorities"] = process.get_dict()["dispose_authorities"].split(" ")
        ret["forms"] = process.get_form_dict()
    else:
        ret["sta"] = 0

    return DjangoHttpRequest.before_send_dispose(ret)


def modify_process(request):
    data = json.loads(request)
    data["process_sid"] = int(data["process_sid"])
    dispose_authorities = copy.deepcopy(data["dispose_authorities"])
    data["dispose_authorities"] = " ".join(data["dispose_authorities"])

    form = ""
    form_dicts = data["form"]
    for form_dict in form_dicts:
        form += form_dict["name"] + "," + form_dict["type"] + "," + form_dict["label"] + ";"
    data["form"] = form[:-1]

    authorities_rows = SqliteMultithread.select(
        """
        SELECT authority_sid, processes FROM authority
        """
    )
    sql_update_sentence = ""
    for authority_row in authorities_rows:
        authority_sid = authority_row[0]
        processes_sid = authority_row[1].split(" ")
        if processes_sid.index(str(data["process_sid"])) is not -1 \
                and dispose_authorities.index(str(authority_sid)) is -1:
            processes_sid.pop(processes_sid.index(str(data["process_sid"])))
            sql_update_sentence += "UPDATE Authority SET processes = '%s' WHERE authority_sid = %d;" \
                                   % (" ".join(processes_sid), int(authority_sid))
        elif processes_sid.index(str(data["process_sid"])) is -1 \
                and dispose_authorities.index(str(authority_sid)) is not -1:
            processes_sid.append(str(data["process_sid"]))
            processes_sid.sort()
            sql_update_sentence += "UPDATE Authority SET processes = '%s' WHERE authority_sid = %d;" \
                                   % (" ".join(processes_sid), int(authority_sid))
    SqliteMultithread.execute(sql_update_sentence)

    SqliteMultithread.execute(
        """
        UPDATE Process SET %s WHERE process_sid = %d
        """ % (Process(data).get_update_format(), data["process_sid"])
    )

    return DjangoHttpRequest.before_send_dispose({})


def upload_business(request):
    data = json.loads(request.POST["data"])
    sid = SqliteMultithread.select("""SELECT COUNT(*) FROM Business""")[0][0] + 1

    processes = ";".join(data["processes"])
    data.pop("processes")

    dispose_departments = " ".join(data["dispose_departments"])
    department_list = data["dispose_departments"]
    for department in department_list:
        rows = SqliteMultithread.select(
            """
            SELECT businesses FROM Department WHERE department_sid = %d
            """ % int(department)
        )
        update_sql_sentence = ""
        for row in rows:
            businesses = row[0]
            if businesses == "":
                businesses = str(sid)
            else:
                businesses += " " + str(sid)
            update_sql_sentence += "UPDATE Department SET businesses = '%s' WHERE department_sid = %d;" \
                                   % (businesses, int(department))
        update_sql_sentence = update_sql_sentence[:-1]
        SqliteMultithread.execute(update_sql_sentence)
    data.pop("dispose_departments")

    business = copy.deepcopy(data)
    business.update({
        "business_sid": sid,
        "dispose_departments": dispose_departments,
        "processes": processes
    })
    SqliteMultithread.execute("""INSERT INTO Business VALUES(%s)""" % Business(business).get_format())

    return DjangoHttpRequest.before_send_dispose({})


def get_business(request):
    data = json.loads(request.POST["data"])
    data["business_sid"] = int(data["business_sid"])
    ret = {
        "sta": 1
    }
    business_rows = SqliteMultithread.select(
        """
        SELECT * FROM Business WHERE business_sid = %d
        """ % data["business_sid"]
    )
    if business_rows.__len__() == 1:
        business = Business(business_rows[0])
        business_dict = business.get_dict()
        ret["dispose_departments"] = business_dict["dispose_department"].split(" ")
        processes_original = business_dict["processes"].split(";")
        processes = []
        for process_original in processes_original:
            processes.append(process_original.split(","))
        ret["processes"] = processes
    else:
        ret["sta"] = 0

    return DjangoHttpRequest.before_send_dispose(ret)


def modify_business(request):
    data = json.loads(request.POST("data"))
    data["business_sid"] = int(data["business_sid"])
    data["processes"] = ";".join(data["processes"])
    dispose_departments = copy.deepcopy(data["dispose_departments"])
    data["dispose_departments"] = " ".join(data["dispose_departments"])

    departments_rows = SqliteMultithread.select(
        """
        SELECT department_sid, businesses FROM Department
        """
    )
    sql_update_sentence = ""
    for department_row in departments_rows:
        department_sid = department_row[0]
        businesses_sid = department_row[1].split(" ")
        if businesses_sid.index(str(data["business_sid"])) is not -1 \
                and dispose_departments.index(department_sid) is -1:
            businesses_sid.pop(businesses_sid.index(str(data["business_sid"])))
            sql_update_sentence += "UPDATE Department SET businesses = '%s' WHERE department_sid = %d;" \
                                   % (" ".join(businesses_sid), int(department_sid))
        elif businesses_sid.index(str(data["business_sid"])) is -1 \
                and dispose_departments.index(department_sid) is not -1:
            businesses_sid.append(str(data["business_sid"]))
            businesses_sid.sort()
            sql_update_sentence += "UPDATE Department SET businesses = '%s' WHERE department_sid = %d;" \
                                   % (" ".join(businesses_sid), int(department_sid))
    SqliteMultithread.execute(sql_update_sentence)

    SqliteMultithread.execute(
        """
        UPDATE Business SET %s WHERE business_sid = %d
        """ % (Business(data).get_update_format(), data["business_sid"])
    )

    return DjangoHttpRequest.before_send_dispose({})


def get_process_table(request):
    ret = {
        "sta": 1,
        "process_table": []
    }

    rows = SqliteMultithread.select("""SELECT * FROM Process""")
    for row in rows:
        process = Process(row)
        process_dict = process.get_dict()
        ret["process_table"].append({
            "process_name": process_dict["process_name"],
            "process_sid": process_dict["process_sid"],
            "dispose_authorities": process_dict["dispose_authorities"].split(" "),
            "form": process.get_form_dict()
        })

    return DjangoHttpRequest.before_send_dispose(ret)


def get_processes(request):
    ret = {
        "sta": 1,
        "processes": []
    }

    rows = SqliteMultithread.select("""SELECT process_name, process_sid FROM Process""")
    for (process_name, process_sid) in rows:
        process = {
            "process_name": process_name,
            "process_sid": process_sid
        }
        ret["processes"].append(copy.deepcopy(process))

    return DjangoHttpRequest.before_send_dispose(ret)


def get_businesses(request):
    ret = {
        "sta": 1,
        "businesses": []
    }

    rows = SqliteMultithread.select("""SELECT business_name, business_sid FROM Business""")
    for (business_name, business_sid) in rows:
        business = {
            "business_name": business_name,
            "business_sid": business_sid
        }
        ret["businesses"].append(copy.deepcopy(business))

    return DjangoHttpRequest.before_send_dispose(ret)
