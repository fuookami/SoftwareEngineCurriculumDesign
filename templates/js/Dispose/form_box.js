/**
 * Created by fuookami on 2017/1/10.
 */

var form_box_handler = function(_boxes_name) {
    var boxes_name = _boxes_name;
    var this_form_format = null;
    var num = 0;

    this.init_form_box = function(_this_form_format) {
        this_form_format = _this_form_format;

        var this_dom_code = "";
        var k = 0;
        for(var i = 0, j = this_form_format.length; i != j; ++i) {
            if (this_form_format[i].label != "application_sid" && this_form_format[i].label != "order_in_application" &&
                this_form_format[i].label != "user_sid" && this_form_format.label != "dispose_time") {
                if(this_form_format[i].label == "bool_box"){
                    this_dom_code += "" +
                            "<p>" +
                                "<label class='LabelText min-indent'>" +
                                this_form_format[i].name + '：' +
                                    "<label class='LabelText'><input type='radio' class='LabelRadio' value='1' name='Data" + k + "'/>是</label>" +
                                    "<label class='LabelText'><input type='radio' class='LabelRadio' value='0' name='Data" + k + "'/>否</label>" +
                                "</label>" +
                            "</p>"
                    ++k;
                }else if(this_form_format[i].label == "number"){
                    this_dom_code += "" +
                        '<label class="LabelText min-indent">' +
                            this_form_format[i].name + '：<input type="number" class="LabelInput" id="Data' + k + '">' +
                        '</label>' +
                        '<br/>'
                    ++k;
                }else if(this_form_format[i].label == "text"){
                    this_dom_code += "" +
                        '<label class="LabelText min-indent">' +
                            this_form_format[i].name + '：<input type="text" class="LabelInput" id="Data' + k + '">' +
                        '</label>' +
                        '<br/>'
                    ++k;
                }else if(this_form_format[i].label == "text_area"){
                    this_dom_code += "" +
                        '<p class="min-indent" style="margin-top: .4em;">' + this_form_format[i].name + '：</p>' +
                        '<textarea id="Data' + k + '" rows="5"></textarea>'
                    ++k;
                }else if(this_form_format[i].label == "datetime"){
                    this_dom_code += "" +
                        '<label class="LabelText min-indent">' +
                            this_form_format[i].name + '：<input type="datetime-local" class="LabelInput" id="Data' + k + '">' +
                        '</label>' +
                        '<br/>'
                    ++k;
                }else{

                }
            }
        }
        num = k;
        jQuery(boxes_name).html(this_dom_code);
    };

    return this;
};