$(function () {

    drawMfGraphs($('#sections'));

    $('#eval-submit').click(function (e) {
        e.preventDefault();

        let data = {},
            $mem = $('#memberships');

        $('#sections').find('.section').each(function () {
            let section = $(this).find('.section-type').val();
            data[section] = getVectors($(this).find('[class^=mf]'), true);

        });

        $mem.val(JSON.stringify(data));
        $('#eval-form').submit();
    });

});