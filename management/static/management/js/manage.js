$(function () {
    let $form = $('#data-by-teacher');

    drawMfGraphs($('#sections'));

    $form.find('button').click(function (e) {
        e.preventDefault();


        let data = {'mfs': {}, 'qs': {}},
            $mem = $form.find('#data');

        $('#sections').find('.section').each(function () {
            let section = $(this).find('.section-type').val();
            data['mfs'][section] = getVectors($(this).find('[class^=mf]'), true);
            data['qs'][section] = [];
        });

        $('.question-list').find('.slider-container input').each(function () {
            let attrs = $(this).prop('name').split('-');
            data['qs'][attrs[1]].push(parseFloat($(this).val()));
        });

        $mem.val(JSON.stringify(data));
        $form.submit();
    });

    $('#acc-upload').change(function () {
        $('#acc-upload-form').submit();
    });

});