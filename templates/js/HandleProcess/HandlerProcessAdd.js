/**
 * Created by fuookami on 2017/1/10.
 */

var server_url = "";
var authority_table = [];
var authority_select_float_box = select_float_box_handler("#DisposeAuthoritiesFloatBoxes", "DisposeAuthority", "负责职位");
var process_form_box = process_form_box_handler("#ProcessFormInfoBoxes", "ProcessForm");

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
    get_authorities();
    process_form_box.init_process_form_box();

    jQuery("#Clear").click(function(){
        location.href = "";
    });

    jQuery("#Upload").click(function(){
        upload_process();
    });
}

function get_authorities() {
    jQuery.ajax({
        type: "POST",
        url: server_url + "manage/get_authorities/",
        async: false,
        dataType: "json",
        data: {
            "data": JSON.stringify({})
        },
        success: function(data) {
            switch(data.sta) {
                case 1:
                    for (var i = 0, j = data.authorities.length; i != j; ++i) {
                        authority_table.push({
                            "sid": data.authorities[i].authority_sid,
                            "display_name": data.authorities[i].authority_name
                        });
                    }
                    authority_select_float_box.init_select_box(authority_table);
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

function upload_process() {
    var data = {
        "process_name": jQuery("#ProcessName").val(),
        "dispose_authorities": authority_select_float_box.get_select_values(),
        "form": process_form_box.get_process_form_values()
    };
    jQuery.ajax({
        type: "POST",
        url: server_url + "manage/upload_process/",
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