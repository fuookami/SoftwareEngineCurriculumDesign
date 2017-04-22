from django.http import HttpResponse
import json


def before_send_dispose(ret):
    response = HttpResponse(json.dumps(ret))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
