$(function() {

    let $q_form = $('#q_form'),
        $sections = $('#sections');

    $q_form.find('ul').sortable();

    let cur_num = 0;
    $q_form.find('.q_form_wrapper').each(function() {
        let numField = $(this).find('input').filter(function() {
           return this.id.match(/id_form-\d*-number/);
        });
        let num = numField.val();

        let $num_tag = $(this).find('.question_num');
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
     * Handler for click on the copy button on the link field
     */
    $('#copy-link-btn').click(function(e) {
        e.preventDefault();
        let $url_field = $(this).parent().parent().find('#eval-url');
        $url_field.select();
        document.execCommand("copy");
        return false;
    });

    $('.question-del-btn').click(function() {
       let $delete_field = $(this).parent().find('input').filter(function() {
           return this.id.match(/id_form-\d*-delete/);
        });

       $delete_field.prop('checked', true);
    });

    drawMfGraphs($sections);

    $('#save-ms-btn').click(function (e) {
        e.preventDefault();

        let data = {},
            labels = {},
            $mem = $('#memberships');

        $sections.find('.section').each(function () {
            let section = $(this).find('.section-type').val();

            data[section] = getVectors($(this).find('[class^=mf]'), true);

            let theLabels = [];
            $(this).find('[name^=label-mf]').each(function () {
                theLabels.push($(this).val());
            });

            labels[section] = theLabels
        });

        $mem.val(JSON.stringify(data));
        $('#labels').val(JSON.stringify(labels));
        $('#mng-form').submit();
    })

});