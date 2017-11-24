let findNum = /^mf(\d+)$/;

$(function() {

    let $q_form = $('#q_form');

    $q_form.find('ul').sortable({
        stop: function() {
            console.log("foo");
        }
    });

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

    $('#sections').find('.section').each(function() {
        let $svgWrapper = $(this).find('.svg-wrapper'),
            svgId = '#' + $svgWrapper.prop('id'),
            o = initSvg(svgId, $svgWrapper.width(), 300),
            x = Array.from(new Array(101), (x, i) => i / 10);
        console.log(svgId);
        let circles = [],
            vs = [],
            $mfs = $(this).find('input'),
            v2 = getVectors($mfs);

        v2.forEach(vec => {
            let vect = [];
            vec.forEach((val, i) => {
                let y;
                if (i === 0 || i === vec.length - 1) {
                    y = 0;
                } else
                    y = 1;
                circles.push({x: val.v, y: y, field: val.field});
                vect.push(val.v);
            });
            vs.push(vect);
        });

        drawMf(vs, x, o);

        drawGrabHandles(circles, o);

        $mfs.change(function () {
            o.svg.selectAll("path").remove();
            vs = getVectors($mfs).map(a => a.map(b => b.v));
            drawMf(vs, x, o);

            d3.selectAll('circle').raise();
        });
    });

});