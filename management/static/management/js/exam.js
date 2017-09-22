$(function() {

    var $q_form = $('#q_form');

    $q_form.find('ul').sortable({
        stop: function() {
            console.log("foo");
        }
    });

    var cur_num = 0;
    $q_form.find('.q_form_wrapper').each(function() {
        var numField = $(this).find('input').filter(function() {
           return this.id.match(/id_form-\d*-number/);
        });
        var num = numField.val();

        var $num_tag = $(this).find('.question_num');
        if(num !== '') {
            num = parseInt(num);
            if (num > cur_num) cur_num = num;
            $num_tag.text(num + ":");
        } else {
            cur_num ++;
            $num_tag.text(cur_num + ":");
            numField.val(cur_num);
        }
    });

    /**
     * Handler for click on the copy buttond on the link field
     */
    $('#copy-link-btn').click(function(e) {
        e.preventDefault();
        var $url_field = $(this).parent().parent().find('#eval-url');
        $url_field.select();
        document.execCommand("copy");
        return false;
    });

    $('.question-del-btn').click(function() {
       var $delete_field = $(this).parent().find('input').filter(function() {
           return this.id.match(/id_form-\d*-delete/);
        });

       $delete_field.prop('checked', true);
    });

});