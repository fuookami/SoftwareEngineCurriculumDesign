/**
 * Created by fuookami on 2017/1/10.
 */

var business_processes_box_handler = function(_boxes_name, _box_name) {
    var boxes_name = _boxes_name;
    var box_name = _box_name;
    var process = [];
    var box_or = 0;
    var box_num = 0;

    this.init_business_processes_box = function(_process) {
        process = _process;

        set_event();
    };

    this.get_business_processes_values = function() {
        var values = [];
        var boxes = jQuery(boxes_name);
        boxes.children(".InfoBox").each(function(i, target){
            var this_box_name = jQuery(target).attr("id");
            values.push(jQuery("#" + this_box_name + "Process").val() + "," + jQuery("#" + this_box_name + "NextOrder").val());
        });
        return values;
    };

    var get_basic_dom_code = function() {
        var dom_code = '';
        dom_code += '<div class="clearfix box InfoBox" id="' + box_name + ++box_or +'">' +
            '<label class="LabelText">' +
                '<label class="labeltext" id="' + box_name + box_or + 'Order">' + ++box_num + '.</label>' +
                '业务流程：' +
                '<select class="LabelSelect" id="' + box_name + box_or + 'Process">' +
                    '<option value="0">结束业务</option>';
        for(var i = 0, j = process.length; i != j; ++i) {
            dom_code += '<option value="' + process[i].process_sid + '">' + process[i].process_name + '</option>';
        }
        dom_code += '' +
                '</select>' +
            '</label>' +
            '<img src="../resource/image/del.png" class="InfoInputBoxDelBtn"/>' +
            '<br/>' +
            '<label class="LabelText">不通过跳转至：' +
                '<select class="LabelSelect" id="' + box_name + box_or + 'NextOrder">' +
                    '<option value="00">结束业务</option>' +
                    '<option value="1">继续业务</option>';
        for(var i = 0; i != box_num; ++i) {
            dom_code += '<option value="0' + (i + 1) + '">跳转至业务流程' + (i + 1) + '</option>';
        }
        dom_code += '' +
                '</select>' +
            '</label>' +
        '</div>';
        return dom_code;
    };

    var set_event = function() {
        var boxes = jQuery(boxes_name);

        boxes.on('click', '.AddProcessBtn', function(e){
            jQuery(e.currentTarget).before(get_basic_dom_code());
            e.preventBubble();
        });

        boxes.on('click', '.InfoInputBoxDelBtn', function(e){
            jQuery(e.currentTarget).parent().remove();
            --box_num;
            boxes.children(".InfoBox").each(function(i, target){
                var this_box_name = jQuery(target).attr("id");
                jQuery("#" + this_box_name + "Order").html(i + 1 + ".");
                var next_order_select = jQuery("#" + this_box_name + "NextOrder");
                next_order_select.html('<option value="00">结束业务</option><option value="1">继续业务</option>');
                for(var j = 0, k = i + 1; j != k; ++j) {
                    next_order_select.append('<option value="0' + (j + 1) + '">跳转至业务流程' + (j + 1) + '</option>');
                }
            });
        });
    };

    return this;
};