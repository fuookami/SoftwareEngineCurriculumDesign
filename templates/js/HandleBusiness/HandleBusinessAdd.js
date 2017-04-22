/**
 * Created by fuookami on 2017/1/10.
 */

var server_url = "";
var department_table = [];
var process_table = [];
var processes = [];
var department_select_float_box = select_float_box_handler("#DisposeDepartmentsFloatBoxes", "DisposerDepartment", "负责部门");
var business_processes_box = business_processes_box_handler("#ProcessesBoxes", "BusinessProcess");

jQuery(document).ready(function(){
    if(!jQuery.cookie("account")) {
        location.href = "../Login.html";
    } else {
        jQuery.getJSON("../../resource/setting.json", function (data) {
            server_url = String(data.server_url);
            run();
        });
    }
});

function run() {
    public_function.add_title_show_hide();
    public_function.set_header();
    get_departments();
    get_processes();

    jQuery("#Clear").click(function(){
        location.href="";
    });

    jQuery("#Upload").click(function(){
        upload_business();
    });
}

function get_departments() {
    jQuery.ajax({
        type: "POST",
        url: server_url + "manage/get_departments/",
        async: false,
        dataType: "JSON",
        data: {
            "data": JSON.stringify({})
        },
        success: function(data) {
            switch(data.sta) {
                case 1:
                    for (var i = 0, j = data.departments.length; i != j; ++i) {
                        department_table.push({
                            "sid": data.departments[i].department_sid,
                            "display_name": data.departments[i].department_name
                        });
                    }
                    department_select_float_box.init_select_box(department_table);
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

function get_processes() {
    jQuery.ajax({
        type: "POST",
        url: server_url + "manage/get_process_table/",
        async: false,
        dataType: "JSON",
        data: {
            "data": JSON.stringify({})
        },
        success: function(data) {
            process_table = data.process_table;
            switch(data.sta) {
                case 1:
                    for (var i = 0, j = process_table.length; i != j; ++i) {
                        processes.push({
                            "process_name": process_table[i].process_name,
                            "process_sid": process_table[i].process_sid
                        })
                    }
                    business_processes_box.init_business_processes_box(processes);
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

function upload_business() {
    var data = {
        "business_name": jQuery("#BusinessName").val(),
        "dispose_departments": department_select_float_box.get_select_values(),
        "processes": business_processes_box.get_business_processes_values()
    };
    jQuery.ajax({
        type: "POST",
        url: server_url + "manage/upload_business/",
        async: false,
        dataType: "JSON",
        data: {
            "data": JSON.stringify(data)
        },
        success: function() {
            alert("上传成功");
            location.href = "";
        },
        error: function() {
            alert("服务器连接失败，请检查网络。");
        }
    })
}