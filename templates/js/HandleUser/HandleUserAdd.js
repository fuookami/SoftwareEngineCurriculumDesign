/**
 * Created by 夏珍妮 on 2017/1/10.
 */

var server_url = "";

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
    get_authorities();

    jQuery("#Close").click(function(){
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
            var department_select = jQuery("#Department");
            switch(data.sta) {
                case 1:
                    for (var i = 0, j = data.departments.length; i != j; ++i) {
                        department_select.append('<option value="' + data.departments[i].department_sid + '">'
                            + data.departments[i].department_name + '</option>');
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
    })
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
            var authority_select = jQuery("#Authority");
            switch(data.sta) {
                case 1:
                    for (var i = 0, j = data.authorities.length; i != j; ++i) {
                        authority_select.append('<option value="' + data.authorities[i].authority_sid + '">'
                            + data.authorities[i].authority_name + '</option>');
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

function upload_business() {
    var data = {
        "name": jQuery("#Name").val(),
        "tel": jQuery("#Tel").val(),
        "mail": jQuery("#Mail").val(),
        "account": jQuery("#Account").val(),
        "password": jQuery("#Password").val(),
        "entry_time": jQuery("#EntryTime").val(),
        "department_sid": jQuery("#Department").val(),
        "authority_sid":  jQuery("#Authority").val()
    };
    jQuery.ajax({
        type: "POST",
        url: server_url + "manage/upload_user/",
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

