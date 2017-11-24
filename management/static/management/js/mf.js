let findNum = /^mf(\d+)$/;

$(function () {
    let $svgWrapper = $("#svg-wrapper"),
        $questionList = $('#question-list'),
        o = initSvg('#svg-wrapper', $svgWrapper.width(), 300),
        x = Array.from(new Array(101), (x, i) => i / 10);


    $questionList.find('a').click(function () {
        o.svg.selectAll('*').remove();

        let circles = [],
            vs = [],
            $mfs = $(this).find('[class^=mf]'),
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
        });

    });

    $questionList.find('a').first().click();


});

