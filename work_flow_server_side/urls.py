"""work_flow_server_side URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from SECD.views import BusinessSubSystem, ManageSubSystem

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', BusinessSubSystem.login, name="login"),

    url(r'^business/get_application_info/', BusinessSubSystem.get_application_info,
        name="business_get_application_info"),
    url(r'^business/upload_form/', BusinessSubSystem.upload_form, name="business_upload_form"),
    url(r'^business/send_notice/', BusinessSubSystem.send_notice, name="business_send_notice"),
    url(r'^business/get_search_key/', BusinessSubSystem.get_search_keys, name="business_get_search_key"),
    url(r'^business/search_get_application_info/', BusinessSubSystem.search_get_application_info,
        name="business_search_get_application_info"),
    url(r'^business/get_process_detail/', BusinessSubSystem.get_process_detail,
        name="business_get_process_detail"),

    url(r'^manage/upload_process/', ManageSubSystem.upload_process, name="manage_upload_process"),
    url(r'^manage/get_process/', ManageSubSystem.get_process, name="manage_get_process"),
    url(r'^manage/modify_process/', ManageSubSystem.modify_process, name="manage_modify_process"),
    url(r'^manage/upload_business/', ManageSubSystem.upload_business, name="manage_upload_business"),
    url(r'^manage/get_business/', ManageSubSystem.get_business, name="manage_get_business"),
    url(r'^manage/modify_business/', ManageSubSystem.modify_business, name="manage_modify_business"),
    url(r'^manage/get_process_table/', ManageSubSystem.get_process_table, name="manage_get_process_table"),
    url(r'^manage/get_processes/', ManageSubSystem.get_processes, name="manage_get_processes"),
    url(r'^manage/get_businesses/', ManageSubSystem.get_businesses, name="manage_get_businesses"),

    url(r'^manage/upload_authority/', ManageSubSystem.upload_authority, name="manage_upload_authority"),
    url(r'^manage/get_authority/', ManageSubSystem.get_authority, name="manage_get_authority"),
    url(r'^manage/modify_authority/', ManageSubSystem.modify_authority, name="manage_modify_authority"),
    url(r'^manage/upload_department/', ManageSubSystem.upload_department, name="manage_upload_department"),
    url(r'^manage/get_department/', ManageSubSystem.get_department, name="manage_get_department"),
    url(r'^manage/modify_department/', ManageSubSystem.modify_department, name="manage_modify_department"),
    url(r'^manage/upload_user/', ManageSubSystem.upload_user, name="manage_upload_user"),
    url(r'^manage/get_user/', ManageSubSystem.get_user, name="manage_get_user"),
    url(r'^manage/modify_user/', ManageSubSystem.modify_user, name="manage_modify_user"),
    url(r'^manage/get_authorities/', ManageSubSystem.get_authorities, name="manage_get_authorities"),
    url(r'^manage/get_departments/', ManageSubSystem.get_departments, name="manage_get_departments")
]
