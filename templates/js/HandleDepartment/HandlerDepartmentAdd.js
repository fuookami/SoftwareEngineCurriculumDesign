/**
 * Created by 于慧慧 on 2017/1/10.
 */
var server_url = "";
var business_table = [];
var business_select_float_box = select_float_box_handler("#BusinessesFloatBoxes", "Business", "处理业务");

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
    get_businesses();

    jQuery("#Clear").click(function(){
        location.href = "";
    });

    jQuery("#Upload").click(function(){
        upload_department();
    });
}

function get_businesses() {
    jQuery.ajax({
        type: "POST",
        url: server_url + "manage/get_businesses/",
        async: false,
        dataType: "json",
        data: {
            "data": JSON.stringify({})
        },
        success: function(data) {
            switch(data.sta) {
                case 1:
                    for (var i = 0, j = data.businesses.length; i != j; ++i) {
                        business_table.push({
                            "sid": data.businesses[i].business_sid,
                            "display_name": data.businesses[i].business_name
                        });
                    }
                    business_select_float_box.init_select_box(business_table);
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

function upload_department() {
    var data = {
        "department_name": jQuery("#DepartmentName").val(),
        "businesses": business_select_float_box.get_select_values(),
    };
    jQuery.ajax({
        type: "POST",
        url: server_url + "manage/upload_department/",
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