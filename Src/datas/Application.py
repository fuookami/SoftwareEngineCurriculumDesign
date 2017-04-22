import datetime
from Src.SqliteMultithread import DataBase, DataTypeBase, data_type_decorator

__metaclass__ = type


@data_type_decorator
class Application(DataTypeBase):
    data_base = DataBase(
        [
            "application_sid", "business_sid",
            "curr_process_sid", "curr_process_order", "has_dispose_process_orders"
        ],
        {
            "application_sid": 0,
            "business_sid": 0,
            "curr_process_sid": 0,
            "curr_process_order": 0,
            "has_dispose_process_orders": "",
        }
    )


@data_type_decorator
class ApplicationContent(DataTypeBase):
    data_base = DataBase(
        [
            "application_sid",
            "apply_time", "accept_final_time", "applicant_type",
            "enterprise_name", "enterprise_certificate_type", "enterprise_certificate_id",
            "applicant_tel", "applicant_site", "applicant_mail",
            "linkman_name", "linkman_certificate_type", "linkman_certificate_id",
            "linkman_tel", "linkman_site", "linkman_postcode", "linkman_mail",
            "product_type", "enterprise_region",
            "reported_application", "business_license", "former_license", "other"
        ],
        {
            "application_sid": 0,

            "apply_time": datetime.datetime.now(),
            "accept_final_time": datetime.datetime.now(),

            "applicant_type": "",

            "enterprise_name": "",
            "enterprise_certificate_type": "",
            "enterprise_certificate_id": "",

            "applicant_tel": "",
            "applicant_site": "",
            "applicant_mail": "",

            "linkman_name": "",
            "linkman_certificate_type": "",
            "linkman_certificate_id": "",
            "linkman_tel": "",
            "linkman_site": "",
            "linkman_postcode": "",
            "linkman_mail": "",

            "product_type": "",
            "enterprise_region": "",

            "reported_application": "",
            "business_license": "",
            "former_license": "",
            "other": ""
        }
    )
