/**
 * Created by fuookami on 2016/12/21.
 */

var application_info_box_handler = function(_box_name){
    var box_name = _box_name;
    var box = null;
    var page_turn_box = null;
    var detail_box_is_visible = false;

    var info = [];
    var application_sid_to_order = {};
    var curr_detail_page_order = -1;
    var curr_detail_order = -1;

    var curr_page = 0;
    var info_per_page = 6;

    this.init_application_info_box = function(_info){
        info = _info;

        var boxes = jQuery(box_name);
        boxes.append(
            '<div class="CurrPageInfoBox ApplicationInfoBox"></div>' +
            '<div class="PageTurnBox">' +
                '<img class="LeftArrow Arrow" src="../resource/image/arrow_normal.png">' +
                '<img class="RightArrow Arrow" src="../resource/image/arrow_normal.png">' +
            '</div>'
            );
        box = boxes.children(".CurrPageInfoBox");
        page_turn_box = boxes.children(".PageTurnBox");

        var page_right_arrow = page_turn_box.children(".RightArrow");
        for(var i = 0, j = info.length/info_per_page; i < j; ++i){
            page_right_arrow.before('<div id="Page' + i +'" class="PageRadius"></div>');
        }
        for(var i = 0, j = info.length; i < j; ++i){
            application_sid_to_order[info[i].application_sid] = i;
        }
        display_curr_page();
        set_event();
    };

    this.clear_application_info_box = function(){
        info = [];
        application_sid_to_order = {};
        curr_detail_order = -1;
        curr_detail_page_order = -1;

        if(box != null)
        {
            box.remove();
            page_turn_box.remove();
        }
        box = null;
        page_turn_box = null;
    };

    this.remove_application_info_curr_detail_box = function() {
        if(curr_detail_page_order != -1){
            box.children("div:eq(" + curr_detail_page_order + ")").removeClass("CurrDetail");
        }
        detail_box_is_visible = false;
        curr_detail_order = -1;
        curr_detail_page_order = -1;
    };

    var display_curr_page = function() {
        box.show();
        for(var i = curr_page * info_per_page, j=(curr_page + 1) * info_per_page,
                k = info.length; i < j && i < k; ++i){
            if(i == curr_detail_order){
                curr_detail_page_order = i - curr_page * info_per_page;
            }
            add_with_value(i);
        }
        box.css("opacity", "0");
        box.animate({opacity: 1}, 150, jQuery.easeInOutCubic);
        jQuery("#Page" + curr_page).animate({color: "#a14b4c"}, 200, jQuery.easeInOutCubic, function(e){
            jQuery(this).addClass("CurrPage");
        });
        if(curr_detail_page_order != -1){
            box.children("div:eq(" + curr_detail_page_order + ")").addClass("CurrDetail");
        }
        page_turn_box.children(".LeftArrow").attr("disabled", curr_page == 0);
        page_turn_box.children(".RightArrow").attr("disabled", curr_page + 1 >= info.length/8);
    };

    var add_with_value = function(i) {
        var this_com_dom_code =
            '<div class="box InfoBox">' +
            '<p><b>申请企业名称：' + info[i].enterprise_name + '</b></p>' +
            '<p>申请时间：' + info[i].apply_time + '</p>' +
            '<p>受理预警时间：' + info[i].accept_final_time + '</p>' +
            '<p>办理业务：' + info[i].business_name + '</p>' +
            '<p>联系人：' + info[i].linkman_name + '</p>' +
            '<p>产品类型：' + info[i].product_type + '</p>' +
            '</div>';
        box.append(this_com_dom_code);
    };

    var shut_curr_page = function() {
        box.animate({opacity: 0}, 150, jQuery.easeInOutCubic, jQuery.proxy(function(){
            box.hide();
            box.html("");
            box.trigger("ShutPageComplete");
        }, this));

        curr_detail_page_order = -1;
        jQuery("#Page" + curr_page).animate({color: "#fff"}, 200, jQuery.easeInOutCubic, function(){
            jQuery(this).removeClass("CurrPage");
        });
    };

    var wait_shut_curr_page = function(target_page){
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

        box.on('click', ".InfoBox", jQuery.proxy(function(e){
            var this_box = jQuery(e.currentTarget);
            if(!this_box.hasClass("CurrDetail")){
                this_box.addClass('CurrDetail');
                if(curr_detail_page_order != -1){
                    this_box.siblings('[class*="CurrDetail"]').removeClass("CurrDetail");
                }
                curr_detail_page_order = this_box.prevAll().length;
                curr_detail_order = info_per_page * curr_page + curr_detail_page_order;

                jQuery(box_name).trigger("OneHasSelect", [{
                    "application_sid": info[curr_detail_order].application_sid
                }]);
            }
        }, this));
    };

    return this;
};