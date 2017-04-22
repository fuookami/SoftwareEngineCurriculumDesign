/**
 * Created by aoki on 2017/1/10.
 */

var server_url = "";
var process_table = [];
var process_select_float_box = select_float_box_handler("#ProcessesFloatBoxes", "Process", "业务流程");

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
    get_processes();

    jQuery("#Clear").click(function(){
        location.href = "";
    });

    jQuery("#Upload").click(function(){
        upload_authority();
    });
}

function get_processes() {
    jQuery.ajax({
        type: "POST",
        url: server_url + "manage/get_processes/",
        async: false,
        dataType: "json",
        data: {
            "data": JSON.stringify({})
        },
        success: function(data) {
            switch(data.sta) {
                case 1:
                    for (var i = 0, j = data.processes.length; i != j; ++i) {
                        process_table.push({
                            "sid": data.processes[i].process_sid,
                            "display_name": data.processes[i].process_name
                        });
                    }
                    process_select_float_box.init_select_box(process_table);
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

function upload_authority() {
    var data = {
        "authority_name": jQuery("#AuthorityName").val(),
        "processes": process_select_float_box.get_select_values()
    };
    jQuery.ajax({
        type: "POST",
        url: server_url + "manage/upload_authority/",
        async: false,
        dataType: "json",
        data : {
            "data": JSON.stringify(data)
        },
        success: function() {
            alert("上传成功");
            location.href = "";
        },
        error: function() {
            alert("服务器连接失败，请检查网络。");
        }
    });
}