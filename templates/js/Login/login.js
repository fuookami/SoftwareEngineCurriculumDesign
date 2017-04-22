/**
 * Created by fuookami on 2016/12/21.
 */

var server_url = String('');

jQuery(document).ready(function(){
    jQuery.getJSON('../resource/setting.json',
        function(data) {
            server_url = String(data.server_url);
            run();
        });

    /*检查是否已经登录了*/
    if(jQuery.cookie("user_sid")){
        if(jQuery.cookie("authority_sid") == 0){
            location.href = "AdminLoginIndex.html";
        }else{

        }
    }
});

function run(){
    jQuery("#AccountInput, #PasswordInput").each(function(){
        jQuery(this).focus(function(){
            if(jQuery(this).hasClass("wrong")){
                jQuery(this).on("input", function(){
                    jQuery(this).removeClass("wrong");
                    jQuery(this).off("input");
                })
            }
        });
    });

    jQuery("#ReturnBtn").click(function(){
        location.href = "Index.html";
    });

    jQuery("#LoginBtn").click(function(){
        var data = {
            "account": jQuery("#AccountInput").val(),
            "password": jQuery("#PasswordInput").val()
        };

        jQuery.ajax({
            type: "POST",
            url: server_url + "login/",
            async: false,
            dataType: "json",
            data: {
                data: JSON.stringify(data)
            },
            beforeSend: function() {
                jQuery("#AccountInput, #PasswordInput").removeClass("wrong");
                jQuery("#LoginStatus").remove();
                jQuery("#LoginBox").prepend('<p id="LoginingStatus">登录中</p>');
            },
            complete: function() {
                jQuery("#LoginingStatus").remove();
            },
            success: function(data) {
                switch(Number(data.sta)) {
                    case 1:
                        jQuery.cookie("account", data.account);
                        jQuery.cookie("user_sid", data.user_sid);
                        jQuery.cookie("department_sid", data.department_sid);
                        jQuery.cookie("authority_sid", data.authority_sid);
                        jQuery.cookie("name", data.name);
                        jQuery.cookie("tel", data.tel);
                        jQuery.cookie("mail", data.mail);
                        jQuery.cookie("entry_date", data.entry_date);
                        if(data.authority_sid == 0) {
                            location.href = "AdminLoginIndex.html";
                        }else{
                            location.href = "LoginIndex.html";
                        }
                        break;
                    case 0:
                        jQuery("#LoginBox").prepend('<p id="LoginStatus">登录失败，请确认密码</p>');
                        jQuery("#PasswordInput").addClass("wrong");
                        break;
                    case 2:
                        jQuery("#LoginBox").prepend('<p id="LoginStatus">登录失败，账号不存在</p>');
                        jQuery("#AccountInput").addClass("wrong");
                        break;
                    default:
                        alert("未知错误");
                        break;
                }
            },
            error : function() {
                jQuery("#LoginStatus").val('链接失败，请确认网络');
            }
        });
    });
}