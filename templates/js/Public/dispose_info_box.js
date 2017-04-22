/**
 * Created by fuookami on 2017/1/10.
 */

var dispose_info_box_handler = function(_boxes_name) {
    var boxes_name = _boxes_name;
    var curr_page = 0;
    var application_detail = {};
    var processes_sid = [];
    var processes_info = [];
    var sid_to_info_order = {};
    var has_dispose_process_orders = [];
    var forms = [];

    this.init_dispose_info_box = function(_application_detail, _processes_sid, _processes_info, _has_dispose_process_orders, _forms) {
        curr_page = 0;
        application_detail = _application_detail;
        processes_sid = _processes_sid;
        processes_info = _processes_info;
        for(var i = 0, j = processes_info.length; i != j; ++i) {
            sid_to_info_order[processes_info[i].process_sid] = i;
        }
        has_dispose_process_orders = _has_dispose_process_orders;
        forms = _forms;

        var boxes = jQuery(boxes_name);
        boxes.append(
            '<div class="CurrPageInfoBox DisposeInfoBox"></div>' +
            '<div class="PageTurnBox">' +
                '<img class="LeftArrow Arrow" src="../resource/image/arrow_normal.png">' +
                '<img class="RightArrow Arrow" src="../resource/image/arrow_normal.png">' +
            '</div>'
        );

        var page_turn_box = boxes.children(".PageTurnBox");

        var page_right_arrow = page_turn_box.children(".RightArrow");
        for(var i = 0, j = _has_dispose_process_orders.length + 1; i < j; ++i){
            page_right_arrow.before('<div id="Page' + i +'" class="PageRadius"></div>');
        }

        display_curr_page();
        set_event();
    };

    var display_curr_page = function() {
        var box = jQuery(boxes_name).children(".DisposeInfoBox");

        if (curr_page == 0) {
            display_application_detail();
        }else {
            display_process_detail();
        }

        box.show();
        box.css("opacity", "0");
        box.animate({opacity: 1}, 150, jQuery.easeInOutCubic);

        var page_turn_box = jQuery(boxes_name).children(".PageTurnBox");
        jQuery("#Page" + (curr_page - 1)).animate({color: "#a14b4c"}, 200, jQuery.easeInOutCubic, function(e){
            jQuery("#Page" + (curr_page - 1)).addClass("CurrPage");
        });
        page_turn_box.children(".LeftArrow").attr("disabled", curr_page == 0);
        page_turn_box.children(".RightArrow").attr("disabled", curr_page - 1 >= has_dispose_process_orders.length);
    };

    var display_application_detail = function() {
        var box = jQuery(boxes_name).children(".DisposeInfoBox");

        var this_dom_code =
                "<p class='SubTitle'><b>业务名称：" + application_detail.business_name + "</b></p>" +
                "<p class='SubTitle'>申请时间：" + application_detail.apply_time + "</p>" +
                "<p class='SubTitle'>受理预警时间：" + application_detail.accept_final_time + "</p>" +
                "<p class='SubTitle'><b>申请信息</b></p>" +
                    "<p class='min-indent'>申请者类型：" + application_detail.applicant_type + "</p>" +
                    "<p class='min-indent'>申请企业信息：</p>" +
                        "<p class='indent'>申请企业名称：" + application_detail.enterprise_name +　"</p>" +
                        "<p class='indent'>申请企业证书类型：" + application_detail.enterprise_certificate_type + "</p>" +
                        "<p class='indent'>申请企业证件号码：" + application_detail.enterprise_certificate_id + "</p>" +
                    "<p class='min-indent'>申请者信息：</p>" +
                        "<p class='indent'>申请者联系方式：" + application_detail.applicant_tel +　"</p>" +
                        "<p class='indent'>申请者地址：" + application_detail.applicant_site + "</p>" +
                        "<p class='indent'>申请者邮箱：" + application_detail.applicant_mail + "</p>" +
                    "<p class='min-indent'>联系人信息：</p>" +
                        "<p class='indent'>联系人姓名：" + application_detail.applicant_tel +　"</p>" +
                        "<p class='indent'>联系人证件类型：" + application_detail.applicant_site + "</p>" +
                        "<p class='indent'>联系人证件号码：" + application_detail.applicant_mail + "</p>" +
                        "<p class='indent'>联系人联系方式：" + application_detail.applicant_tel +　"</p>" +
                        "<p class='indent'>联系人地址：" + application_detail.applicant_site + "</p>" +
                        "<p class='indent'>联系人邮编：" + application_detail.applicant_mail + "</p>" +
                        "<p class='indent'>联系人邮箱：" + application_detail.applicant_mail + "</p>" +
                    "<p class='min-indent'>产品类型：" + application_detail.product_type + "</p>" +
                    "<p class='min-indent'>企业所属地区：" + application_detail.enterprise_region + "</p>"
        // reported_application, business_license, former_license, other
            ;
        box.html(this_dom_code);
    };

    var display_process_detail = function() {
        var box = jQuery(boxes_name).children(".DisposeInfoBox");

        var curr_sid = processes_sid[has_dispose_process_orders[curr_page - 1]];
        var curr_order = sid_to_info_order[curr_sid];
        var curr_form_format = processes_info[curr_order].form;
        var curr_form = forms[curr_page - 1];
        var this_dom_code =
            "<p class='SubTitle'><b>业务流程：" + processes_info[curr_order].process_name + "</b>";
        for(var i = 0, j = curr_form_format.length; i < j; ++i) {
            if(curr_form_format[i].label != "application_sid" && curr_form_format[i].label != "order_in_application") {
                if(curr_form_format[i].label == "user_sid"){
                    this_dom_code += "<p class='min-indent'>处理人:" + curr_form[i] + "</p>";
                }else{
                    this_dom_code += "<p class='min-indent'>" + curr_form_format[i].name + ":" + curr_form[i] + "</p>";
                }
            }
        }

        box.html(this_dom_code);
    };

    var shut_curr_page = function() {
        var box = jQuery(boxes_name).children(".DisposeInfoBox");

        box.animate({opacity: 0}, 150, jQuery.easeInOutCubic, jQuery.proxy(function(){
            box.hide();
            box.html("");
            box.trigger("ShutPageComplete");
        }, this));

        jQuery("#Page" + (curr_page - 1)).animate({color: "#fff"}, 200, jQuery.easeInOutCubic, function(){
            jQuery("#Page" + (curr_page - 1)).removeClass("CurrPage");
        });
    };

    var wait_shut_curr_page = function(target_page){
        var box = jQuery(boxes_name).children(".DisposeInfoBox");

        box.on("ShutPageComplete", jQuery.proxy(function(e){
            curr_page = target_page;
            display_curr_page();
            jQuery(e.currentTarget).off("ShutPageComplete");
        }, this));
    };

    var turn_to_page = function(target_page) {
        if(curr_page != -1) {
            shut_curr_page();
            wait_shut_curr_page(target_page);
        }else {
            curr_page = target_page;
            display_curr_page();
        }
    };

    var set_event = function() {
        var page_turn_box = jQuery(boxes_name).children(".PageTurnBox");

        page_turn_box.children("img").hover(function(e){
            if(!jQuery(e.currentTarget).attr("disabled")){
                jQuery(e.currentTarget).attr("src", "../resource/image/arrow_hover.png");
            }
        }, function(e){
            jQuery(e.currentTarget).attr("src", "../resource/image/arrow_normal.png");
        });

        page_turn_box.on('click', 'img', jQuery.proxy(function(e){
            if(!jQuery(e.currentTarget).attr("disabled")){
                shut_curr_page();
                var target = jQuery(e.currentTarget);
                var isLeftArrow = target.hasClass("LeftArrow");
                var isRightArrow = target.hasClass("RightArrow");
                wait_shut_curr_page(curr_page + (isLeftArrow ? -1 :
                        isRightArrow ? 1 : 0));
            }
        }, this));

        page_turn_box.on('click', 'div', jQuery.proxy(function(e){
            if(!jQuery(e.currentTarget).hasClass("CurrPage")){
                turn_to_page(jQuery(e.currentTarget).prevAll('div').length);
            }
        }, this));
    };

    return this;
};