/**
 * Created by fuookami on 2017/1/10.
 */


var process_form_box_handler = function(_boxes_name, _box_name) {
    var boxes_name = _boxes_name;
    var box_name = _box_name;
    var box_or = 0;
    var labels = ["bool_box", "number", "text", "text_area", "datetime", "date"];
    var types = ["int", "int", "text", "text", "datetime", "date"];

    this.init_process_form_box = function() {
        set_event();
    };

    this.get_process_form_values = function() {
        var values = [{'type': 'int', 'label': 'bool_box', 'name': '是否通过'}];
        jQuery(boxes_name).children(".InfoBox").each(function(i, target){
            var this_box_name = jQuery(target).attr("id");
            var select_value = jQuery("#" + this_box_name + "Label").val();
            values.push({
                "name": jQuery("#" + this_box_name + "Name").val(),
                "label": labels[select_value],
                "type": types[select_value]
            })
        });
        return values;
    };

    var get_basic_dom_code = function(or_str) {
        return '' +
            '<div id="' + box_name + or_str + '" class="clearfix box InfoBox">' +
                '<label class="LabelText">数据名字：<input type="text" id="' + box_name + or_str + 'Name" class="LabelInput"></label>' +
                '<label class="LabelText">数据类型：</label>' +
                '<select id="' + box_name + or_str + 'Label" class="LabelSelect">' +
                    '<option value=0>布尔值</option>' +
                    '<option value=1>数值</option>' +
                    '<option value=2>单行文本</option>' +
                    '<option value=3>多行文本</option>' +
                    '<option value=4>日期-时间</option>' +
                    '<option value=5>日期</option>' +
                '</select>' +
                '<img src="../resource/image/del.png" class="InfoInputBoxDelBtn"/>' +
            '</div>';
    };

    var set_event = function() {
        var boxes = jQuery(boxes_name);

        boxes.on('click', '.AddFormLabelBtn', function(e){
            var or_str = box_name + ++box_or;
            jQuery(e.currentTarget).before(get_basic_dom_code(or_str));
            e.preventBubble();
        });

        boxes.on('click', '.InfoInputBoxDelBtn', function(e){
            jQuery(e.currentTarget).parent().remove();
        });
    };

    return this;
};