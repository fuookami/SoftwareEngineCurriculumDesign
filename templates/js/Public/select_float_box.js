/**
 * Created by fuookami on 2016/9/10.
 */

var select_float_box_handler = function(_float_boxes_name, _float_box_name, _select_for) {
    var float_boxes_name = _float_boxes_name;
    var float_box_name = _float_box_name;
    var select_for = _select_for;
    var box_or = 0;
    var max_select = 0;
    var min_select = 0;

    var dict_list = [];
    var sid_to_display_name = {};
    var display_name_to_sid = {};
    var display_name_to_or = {};
    var list_flag = [];

    this.init_select_box = function(_dict_list, _max_select, _min_select){
        dict_list = _dict_list;
        for(var i = 0, j = dict_list.length; i < j; ++i){
            sid_to_display_name[dict_list[i].sid] = dict_list[i].display_name;
            display_name_to_sid[dict_list[i].display_name] = dict_list[i].sid;
            display_name_to_or[dict_list[i].display_name] = i;
            list_flag[i] = true;
        }

        max_select = _max_select || 0;
        min_select = _min_select || 0;

        set_event();
    };

    this.dest = function(){
        clear();
        off_event();

        box_or = 0;
        max_select = 0;
        min_select = 0;

        dict_list = [];
        sid_to_display_name = {};
        display_name_to_sid = {};
        display_name_to_or = {};
        list_flag = [];
    };

    this.modify_dict_list = function(_dict_list){
        clear();
        dict_list = _dict_list;

        sid_to_display_name = {};
        display_name_to_sid = {};
        display_name_to_or = {};
        list_flag = [];
        for(var i = 0, j = dict_list.length; i < j; ++i){
            sid_to_display_name[dict_list[i].sid] = dict_list[i].display_name;
            display_name_to_sid[dict_list[i].display_name] = dict_list[i].sid;
            display_name_to_or[dict_list[i].display_name] = i;
            list_flag[i] = true;
        }
    };

    this.add_with_value = function(value){
        var or_str = float_box_name + ++box_or;
        var display_name = sid_to_display_name[value];
        var box_dom_code =
            '<div id="' + or_str + '">' +
                '<div class="FloatBox">' +
                    '<select class="LabelSelect"></select>' +
                    '<span>' + display_name + '</span>' +
                    '<img src="../resource/image/del.png" class="FloatBoxDelBtn"/>' +
                '</div>'+
            '</div>';
        jQuery(float_boxes_name).children('.FloatBoxAddBtn').before(box_dom_code);
        jQuery("#" + or_str + ">div>select").hide();
        list_flag[display_name_to_or[display_name]] = false;
    };

    this.get_select_values = function(){
        var values = [];
        jQuery(float_boxes_name).children('div').children(".FloatBox").each(jQuery.proxy(function(i, target){
            values.push(String(display_name_to_sid[jQuery(target).children("span").html()]));
        }, this));
        values.sort();
        return values;
    };

    var clear = function(){
        var add_btn = jQuery(float_boxes_name).children('.FloatBoxAddBtn');
        add_btn.siblings().remove();
        if(add_btn.is(":hidden")){
            add_btn.show();
        }
        box_or = 0;
        for(var i = 0, j = list_flag.length; i < j ; ++i){
            list_flag[i] = true;
        }
    };

    var set_event = function(){

        var float_boxes = jQuery(float_boxes_name);

        float_boxes.on('click', '.FloatBoxAddBtn', jQuery.proxy(function(e){
            var or_str = float_box_name + ++box_or;
            var float_box_num = jQuery(e.currentTarget).siblings().length;
            if(max_select != 0 && float_box_num !=0 && float_box_num == max_select){
                alert("不能添加更多的" + select_for + "了。");
            }else {
                var has_more = false;
                for(var i = 0, j = list_flag.length; i < j && !has_more; ++i){
                    has_more = list_flag[i];
                }
                if(!has_more){
                    alert("没有更多的"+ select_for +"可以添加的了。");
                }else{
                    var box_dom_code =
                        '<div id="' + or_str + '">' +
                            '<div class="FloatBox">' +
                                '<select class="LabelSelect"></select>' +
                                '<span></span>' +
                                '<img src="../resource/image/del.png" class="FloatBoxDelBtn"/>' +
                            '</div>' +
                        '</div>';
                    var add_btn = jQuery(e.currentTarget);
                    add_btn.before(box_dom_code);

                    var max_length = 0;
                    var selector = [];
                    for(var i = 0, j = dict_list.length; i < j; ++i){
                        if(list_flag[i]){
                            selector.push("<option value=" + i + ">" + dict_list[i].display_name + "</option>");
                            if(dict_list[i].display_name.length > max_length){
                                max_length = dict_list[i].display_name.length;
                            }
                        }
                    }

                    var this_box = jQuery("#" + or_str);
                    this_box.children('div').children('span').hide();
                    var select = this_box.children('div').children('select');

                    select.append(selector.join(''));
                    select.val(-1);
                    max_length = (max_length < 7) ? 7 : max_length;
                    select.css("width", max_length + "em");
                    select.focus().select();

                    if(min_select != 0 && (float_box_num + 1) == min_select){
                        jQuery("#" + or_str).addClass("RightMost");
                    }

                    if(max_select != 0 && (float_box_num + 1) == max_select){
                        jQuery("#" + or_str).addClass("RightMost");
                        jQuery(e.currentTarget).hide();
                    }
                }
            }
        }, this));

        float_boxes.on('click', '.FloatBoxDelBtn', jQuery.proxy(function(e){
            var box = jQuery(e.currentTarget).parent().parent();
            var display = jQuery(e.currentTarget).siblings("span");
            var display_name = display.html();
            if(display_name.length){
                list_flag[display_name_to_or[display_name]] = true;
            }
            var add_btn = box.siblings(".FloatBoxAddBtn");
            add_btn.show();
            box.remove();

            if(display_name.length){
                float_boxes.trigger("OneHasShut", [display_name_to_sid[display_name], display_name]);
            }
        }, this));

        float_boxes.on('dblclick', 'span', jQuery.proxy(function(e){
            var display = jQuery(e.currentTarget);
            var select = display.siblings('select');
            var max_length = display.html();
            display.hide();
            select.show();

            var display_name = display.html();
            var curr_select_val = display_name_to_or[display_name];
            list_flag[curr_select_val] = true;
            var selector = [];
            for(var i = 0, j = dict_list.length; i < j; ++i){
                if(list_flag[i]){
                    selector.push("<option value=" + i + ">" + dict_list[i].display_name + "</option>");
                    if(dict_list[i].display_name > max_length){
                        max_length = dict_list[i].display_name;
                    }
                }
            }
            select.append(selector.join());
            select.val(curr_select_val);
            max_length = (max_length < 7) ? 7 : max_length;
            select.css("width", max_length + "em");
            select.focus().select();

            float_boxes.trigger("OneHasShut", [display_name_to_sid[display_name], display_name]);
        }, this));

        float_boxes.on('change', 'select', jQuery.proxy(function(e){
            var select = jQuery(e.currentTarget);
            var display = select.siblings('span');
            var selected = select.val();
            var display_name = dict_list[selected].display_name;
            display.html(display_name);
            list_flag[selected] = false;
            select.hide();
            select.children().remove();
            display.show();
            float_boxes.children(".FloatBox").each(function(){
                var this_select = jQuery(this).children("select");
                var del_child = this_select.children("option[value=" + selected +"]");
                if(del_child.length){
                    del_child.remove();
                    this_select.val(-1);
                }
            });

            float_boxes.trigger("OneHasSelect", [display_name_to_sid[display_name], display_name]);
        }, this));

        float_boxes.on('blur', 'select', jQuery.proxy(function(e) {
            setTimeout(jQuery.proxy(function() {
                var select = jQuery(e.currentTarget);
                var display = select.siblings('span');
                if(display.is(":hidden")){
                    if(select.val() == null){
                        var this_box = select.parent().parent();
                        this_box.siblings(".FloatBoxAddBtn").show();
                        this_box.remove();
                    }else{
                        var selected = select.val();
                        var display_name = dict_list[selected].display_name;
                        display.html(display_name);
                        list_flag[selected] = false;
                        select.hide();
                        select.children().remove();
                        display.show();
                        float_boxes.children(".FloatBox").each(function(){
                            var this_select = jQuery(this).children("select");
                            var del_child = this_select.children("option[value=" + selected +"]");
                            if(del_child.length){
                                del_child.remove();
                                this_select.val(-1);
                            }
                        });

                        float_boxes.trigger("OneHasSelect", [display_name_to_sid[display_name], display_name]);
                    }
                }
            }, this), 100);
        }, this));
    };

    var off_event = function(){
        var box = jQuery(float_boxes_name);

        box.off('click');
        box.off("dblclick");
        box.off('change');
        box.off('blur');
    };

    return this;
};