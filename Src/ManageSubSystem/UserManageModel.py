import json
import copy
from Src import SqliteMultithread
from Src import DjangoHttpRequest
from Src.datas import Authority, Department, User


def upload_authority(request):
    data = json.loads(request.POST["data"])
    sid = SqliteMultithread.select("""SELECT COUNT(*) FROM Authority""")[0][0] + 1

    processes = " ".join(data["processes"])
    process_list = data["processes"]
    for process in process_list:
        rows = SqliteMultithread.select(
            """
            SELECT dispose_authorities FROM Process WHERE process_sid = %d
            """ % int(process)
        )
        upload_sql_sentence = ""
        for row in rows:
            dispose_authorities = row[0]
            if dispose_authorities == "":
                dispose_authorities = str(sid)
            else:
                dispose_authorities += " " + str(sid)
            upload_sql_sentence += "UPDATE Process SET dispose_authorities = '%s' WHERE process_sid = %d" \
                                   % (dispose_authorities, int(process))
        SqliteMultithread.execute(upload_sql_sentence)
    data.pop("processes")

    authority = copy.deepcopy(data)
    authority.update({
        "authority_sid": sid,
        "processes": processes
    })
    SqliteMultithread.execute("""INSERT INTO Authority VALUES (%s)""" % Authority(authority).get_format())

    return DjangoHttpRequest.before_send_dispose({})


def get_authority(request):
    data = json.loads(request)
    data["authority_sid"] = int(data["authority_sid"])
    ret = {
        "sta": 1,
    }

    authority_row = SqliteMultithread.select(
        """
        SELECT * FROM Authority WHERE authority_sid = %d
        """ % data["authority_sid"]
    )

    if authority_row.__len__() == 1:
        authority_dict = Authority(authority_row[0]).get_dict()
        ret["processes"] = authority_dict["processes"].split(" ")
    else:
        ret["sta"] = 0

    return DjangoHttpRequest.before_send_dispose(ret)


def modify_authority(request):
    data = json.loads(request)
    data["authority_sid"] = int(data["authority_sid"])
    processes = copy.deepcopy(data["processes"])
    data["processes"] = " ".join(data["processes"])

    processes_rows = SqliteMultithread.select(
        """
        SELECT process_sid, dispose_authorities FROM Process
        """
    )
    sql_update_sentence = ""
    for process_row in processes_rows:
        process_sid = process_row[0]
        dispose_authorities = process_row[1].split(" ")
        if dispose_authorities.index(str(data["authority_sid"])) is not -1 \
                and processes.index(str(process_sid)) is -1:
            dispose_authorities.pop(dispose_authorities.index(str(data["authority_sid"])))
            sql_update_sentence += "UPDATE Process SET dispose_authorities = '%s' WHERE process_sid = %d;" \
                                   % (" ".join(dispose_authorities), int(process_sid))
        elif dispose_authorities.index(str(data["authority_sid"])) is -1 \
                and processes.index(str(process_sid)) is not -1:
            dispose_authorities.append(str(data["authority_sid"]))
            dispose_authorities.sort()
            sql_update_sentence += "UPDATE Process SET dispose_authorities = '%s' WHERE process_sid = %d;" \
                                   % (" ".join(dispose_authorities), int(process_sid))
    SqliteMultithread.execute(sql_update_sentence)

    SqliteMultithread.execute(
        """
        UPDATE Authority SET %s WHERE authority_sid = %d
        """ % (Authority(data).get_update_format(), data["authority_sid"])
    )

    return DjangoHttpRequest.before_send_dispose({})


def upload_department(request):
    data = json.loads(request.POST["data"])
    sid = SqliteMultithread.select("""SELECT COUNT(*) FROM Department""")[0][0] + 1

    businesses = " ".join(data["businesses"])
    business_list = data["businesses"]
    for business in business_list:
        rows = SqliteMultithread.select(
            """
            SELECT dispose_departments FROM Business WHERE business_sid = %d
            """ % int(business)
        )
        upload_sql_sentence = ""
        for row in rows:
            dispose_departments = row[0]
            if dispose_departments == "":
                dispose_departments = str(sid)
            else:
                dispose_departments += " " + str(sid)
            upload_sql_sentence += "UPDATE Business SET dispose_departments = '%s' WHERE business_sid = %d;" \
                                   % (dispose_departments, int(business))
        SqliteMultithread.execute(upload_sql_sentence)
    data.pop("businesses")

    department = copy.deepcopy(data)
    department.update({
        "department_sid": sid,
        "businesses": businesses
    })
    SqliteMultithread.execute("""INSERT INTO Department VALUES(%s)""" % Department(department).get_format())

    return DjangoHttpRequest.before_send_dispose({})


def get_department(request):
    data = json.loads(request.POST["data"])
    data["department_sid"] = int(data["department_sid"])
    ret = {
        "sta": 1
    }

    department_rows = SqliteMultithread.select(
        """
        SELECT * FROM Department WHERE department_sid = %d
        """ % (data["department_sid"])
    )
    if department_rows.__len__() == 1:
        ret["businesses"] = Department(department_rows[0]).get_dict()["businesses"].split(" ")
    else:
        ret["sta"] = 0

    return DjangoHttpRequest.before_send_dispose(ret)


def modify_department(request):
    data = json.loads(request.POST["data"])
    data["department_sid"] = int(data["department_sid"])
    businesses = copy.deepcopy(data["businesses"])
    data["businesses"] = " ".join(data["businesses"])

    businesses_rows = SqliteMultithread.select(
        """
        SELECT business_sid, dispose_departments FROM Businesses
        """
    )
    sql_update_sentence = ""
    for business_row in businesses_rows:
        business_sid = business_row[0]
        dispose_departments = business_row[1].split(" ")
        if dispose_departments.index(str(data["department_sid"])) is not -1 \
                and businesses.index(business_sid) is -1:
            dispose_departments.pop(dispose_departments.index(str(data["department_sid"])))
            sql_update_sentence += "UPDATE Business SET dispose_departments = '%s' WHERE business_sid = %d;" \
                                   % (" ".join(dispose_departments), int(business_sid))
        elif dispose_departments.index(str(data["department_sid"])) is -1 \
                and businesses.index(business_sid) is not -1:
            dispose_departments.append(str(data["department_sid"]))
            dispose_departments.sort()
            sql_update_sentence += "UPDATE Business SET dispose_departments = '%s' WHERE business_sid = %d;" \
                                   % (" ".join(dispose_departments), int(business_sid))
    SqliteMultithread.execute(sql_update_sentence)

    SqliteMultithread.execute(
        """
        UPDATE Department SET %s WHERE department_sid = %d
        """ % (Department(data).get_update_format(), data["department_sid"])
    )

    return DjangoHttpRequest.before_send_dispose({})


def upload_user(request):
    data = json.loads(request.POST["data"])
    sid = SqliteMultithread.select("""SELECT COUNT(*) FROM User""")[0][0]

    user = copy.deepcopy(data)
    user.update({
        "user_sid": sid
    })
    SqliteMultithread.execute("""INSERT INTO User VALUES(%s)""" % User(user).get_format())

    return DjangoHttpRequest.before_send_dispose({})


def get_user(request):
    data = json.loads(request.POST["data"])
    data["user_sid"] = int(data["user_sid"])
    ret = {
        "sta": 1
    }

    users_rows = SqliteMultithread.select(
        """
        SELECT * FROM User WHERE user_sid = %d
        """ % data["user_sid"]
    )
    if users_rows.__len__() == 1:
        user_dict = User(users_rows).get_dict()
        user_dict.pop("account")
        user_dict.pop("password")
        user_dict.pop("entry_date")
        ret["user"] = user_dict
    else:
        ret["sta"] = 0

    return DjangoHttpRequest.before_send_dispose(ret)


def modify_user(request):
    data = json.loads(request.POST["data"])
    data["user_sid"] = int(data["user_sid"])
    data["department_sid"] = int(data["department_sid"])
    data["authority_sid"] = int(data["authority_sid"])
    ret = {
        "sta": 1
    }

    user_row = SqliteMultithread.select(
        """
        SELECT * FROM User WHERE user_sid = %d
        """ % data["user_sid"]
    )
    user_dict = User(user_row)
    user_dict.update(data)
    SqliteMultithread.execute(
        """
        UPDATE User SET %s WHERE user_sid = %d
        """ % (User(user_dict).get_update_format(), data["user_sid"])
    )

    return DjangoHttpRequest.before_send_dispose({})


def get_authorities(request):
    ret = {
        "sta": 1,
        "authorities": []
    }
    rows = SqliteMultithread.select("""SELECT authority_name, authority_sid FROM Authority""")
    for (authority_name, authority_sid) in rows:
        authority = {
            "authority_name": authority_name,
            "authority_sid": authority_sid
        }
        ret["authorities"].append(copy.deepcopy(authority))

    return DjangoHttpRequest.before_send_dispose(ret)


def get_departments(request):
    ret = {
        "sta": 1,
        "departments": []
    }
    rows = SqliteMultithread.select("""SELECT department_name, department_sid FROM Department""")
    for (department_name, department_sid) in rows:
        department = {
            "department_name": department_name,
            "department_sid": department_sid
        }
        ret["departments"].append(copy.deepcopy(department))

    return DjangoHttpRequest.before_send_dispose(ret)


def get_users(request):
    ret = {
        "sta": 1,
        "users": []
    }
    rows = SqliteMultithread.select("""SELECT user_sid, name FROM User WHERE user_sid != 0""")
    for (user_sid, name) in rows:
        user = {
            "user_name": name,
            "user_sid": user_sid
        }
        ret["users"].append(copy.deepcopy(user))

    return DjangoHttpRequest.before_send_dispose(ret)
