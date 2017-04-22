/**
 * Created by fuookami on 2016/12/22.
 */

var public_function = {
    bool_to_dom_code: function(flag) {
        if(flag == 1) {
            return "<img class='LabelImage' src='resource/image/right.png'>是";
        }else{
            return "<img class='LabelImage' src='resource/image/del.png'>否";
        }
    },

    add_title_show_hide: function() {
        jQuery(".BoxTitleBox").click(function(e){
            var title = jQuery(e.currentTarget).parent();
            if(title.next().is(":hidden")) {
                title.siblings().show();
            }else {
                title.siblings().hide();
            }
        });
    },

    set_header: function() {
        jQuery("a[class*='CurrPage']").click(function (e) {
            e.preventDefault();
        })
    }
};