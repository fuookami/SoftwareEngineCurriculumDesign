/**
 * Created by fuookami on 2017/1/10.
 */

var server_url = "";
var curr_application_sid = 0;
var application_info_box = application_info_box_handler("#ApplicationBoxes");
var dispose_info_box = dispose_info_box_handler("#DisposeBoxes");
var form_box = form_box_handler("#FormBoxes");

var next_process = null;
var processes_sid = null;
var curr_process_order = 0;
var order_in_application = 0;
var curr_process_sid = 0;
var data_num = 0;
var this_form = null;

jQuery(document).ready(function(){
    if(!jQuery.cookie("account")) {
        location.href = "Login.html";
    } else {
        jQuery.getJSON("../resource/setting.json", function (data) {
            server_url = String(data.server_url);
            run();
        });
    }
});

function run() {
    public_function.add_title_show_hide();
    public_function.set_header();

    get_application_info();

    jQuery("#ApplicationInfoBoxes").bind('OneHasSelect', function(e, arg){
        clear();
        curr_application_sid = arg.application_sid;
        get_dispose_info();
        jQuery("#ApplicationBoxes").hide();
    });

    jQuery("#Upload").click(function(){
        upload_form();
    });
}

function clear() {

}

function get_application_info() {
    var data = {
        "department_sid": jQuery.cookie("department_sid"),
        "authority_sid": jQuery.cookie("authority_sid")
    };
    jQuery.ajax({
        type: "POST",
        url: server_url + "business/get_application_info/",
        async: false,
        dataType: "json",
        data: {
            "data": JSON.stringify(data)
        },
        success: function(data) {
            switch(data.sta) {
                case 1:
                    application_info_box.init_application_info_box(data.application_info);
                    break;
                default:
                    alert("未知错误。");
                    break;
            }
        },
        error: function() {
            alert("服务器连接失败，请检查网络。");
        }
    })
}

function get_dispose_info() {
    var data = {
        "application_sid": curr_application_sid
    };
    jQuery.ajax({
        type: "POST",
        url: server_url + "business/get_process_detail/",
        async: false,
        dataType: "json",
        data: {
            "data": JSON.stringify(data)
        },
        success: function(data) {
            next_process = data.dispose_info.next_process;
            curr_process_order = data.dispose_info.curr_process_order;
            processes_sid = data.dispose_info.processes_sid;
            order_in_application = data.dispose_info.has_dispose_process_orders.length;
            curr_process_sid = processes_sid[curr_process_order - 1];
            switch(data.sta) {
                case 1:
                    var processes_info = data.dispose_info.processes_info;
                    dispose_info_box.init_dispose_info_box(data.application_detail, processes_sid, processes_info,
                        data.dispose_info.has_dispose_process_orders, data.dispose_info.forms);

                    for(var i = 0, j = processes_info.length; i != j; ++i){
                        if(processes_info[i].process_sid == curr_process_sid){
                            this_form = processes_info[i].form;
                            data_num = processes_info[i].form.length - 4;
                            form_box.init_form_box(processes_info[i].form);
                        }
                    }
                    break;
                default:
                    alert("未知错误。");
                    break;
            }
        },
        error: function() {
            alert("服务器连接失败，请检查网络。");
        }
    });
}

function upload_form() {
    var data = {
        "user_sid": jQuery.cookie("user_sid"),
        "application_sid": curr_application_sid,
        "order_in_application": order_in_application,
        "curr_order": curr_process_order,
        "process_sid": curr_process_sid
    };
    if(jQuery("Input:checked[name='Data0']").val()) {
        data["next_order"] = curr_process_order + 1;
        data["next_sid"] = next_process.over_sid;
    }else {
        data["next_order"] = next_process.not_over_order;
        data["next_sid"] = next_process.not_over_order == 0 ? 0 : processes_sid[next_process.not_over_order - 1];
    }
    for(var i = 0; i != data_num; ++i) {
        if(this_form[i + 4].label == "bool_box"){
            data["data" + i] = jQuery("Input:checked[name='Data" + i + "']").val();
        }else{
            data["data" + i] = jQuery("#Data" + i).val();
        }
    }

    jQuery.ajax({
        type: "POST",
        url: server_url + "business/upload_form/",
        dataType: "json",
        data: {
            "data": JSON.stringify(data)
        },
        success: function(data) {
            alert("上传成功");
            location.href = "";
        },
        error: function() {
            alert("服务器连接失败，请检查网络。");
        }
    })
};