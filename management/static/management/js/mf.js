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

function getVectors($fields) {
    let vect = [];

    $fields.each(function () {
        let eleClass = $(this).prop('class');
        let num = parseInt(findNum.exec(eleClass)[1]),
            i = num - 1;

        if (typeof vect[i] === 'undefined') {
            vect[i] = [];
        }

        vect[i].push({v: $(this).val(), field: $(this)});
    });

    return vect;
}

function drawMf(v, x, o) {
    let data = [];

    v.forEach(vx => {
        let temp = [];
        x.forEach(n => {
            temp.push({xData: n, yData: mf(n, vx)})
        });
        data.push(temp);
    });

    drawLineGraph(data, o);
}


function mf(x, v) {

    let a = v[0],
        b = v[1];

    let k = (x - a) / (b - a);

    if (v.length === 2) {
        return Math.max(Math.min(k, l), 0);
    } else {

        let c = v[2];

        if (v.length === 3) {
            let l = (c - x) / (c - b);

            return Math.max(Math.min(k, l), 0)
        } else if (v.length === 4) {
            let d = v[3],
                n = (d - x) / (d - c);

            return Math.max(Math.min(Math.min(k, n), 1), 0)
        }

    }

}

function initSvg(selector, width, height) {
    let obj = {};
    let svg = d3.select(selector).append('svg')
            .attr('width', width)
            .attr('height', height),
        margin = {top: 20, right: 20, bottom: 30, left: 50},
        w = width - margin.left - margin.right,
        h = height - margin.top - margin.bottom;

    obj.svg = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    obj.x = d3.scaleLinear()
        .range([0, w]);

    obj.y = d3.scaleLinear()
        .range([h, 0]);

    obj.height = h;
    obj.width = w;

    return obj;
}

function drawGrabHandles(data, o) {

    let y = o.y
        .domain(d3.extent(data, function (d) {
            return d.y;
        }));

    let x = o.x
        .domain(d3.extent(data, function (d) {
            return d.x;
        }));
    o.svg.selectAll("circles")
        .data(data)
        .enter().append("circle")
        .attr("cx", function (d) {
            return x(d.x - 1);
        })
        .attr("cy", function (d) {
            return y(d.y);
        })
        .attr("r", 8)
        .style("fill", function (d, i) {
            return "#550000";
        })
        .call(d3.drag().subject(function () {
            let t = d3.select(this);
            return {x: t.attr("cx"), y: t.attr("cy")}
        })
            .on("drag", function (d) {
                let curVal = parseInt(d.field.val()),
                    eventVal = d3.event.x,
                    newTemp = o.x.invert(eventVal),
                    newVal = Math.round(newTemp);
                if (newVal !== curVal) {
                    d.field.val(newVal);
                    d.field.change();
                    d3.select(this).attr("cx", d.x = x(newVal));
                }

            }))

}


function drawLineGraph(data, o) {
    let colors = ['#00aa00', '#dddd00', '#ffaa00', '#aa0000'];
    let legend = ['Easy', 'Fair', 'Hard', 'Very Hard'];

    let y = o.y
        .domain(d3.extent(data[0], function (d) {
            return d.yData;
        }));

    let x = o.x
        .domain(d3.extent(data[0], function (d) {
            return d.xData;
        }));

    let xAxis = d3.axisBottom()
        .scale(x);

    let yAxis = d3.axisLeft()
        .scale(y);

    o.svg.append("g")
        .call(yAxis);

    o.svg.append("g")
        .attr("transform", "translate(0," + o.height + ")")
        .call(xAxis);

    data.forEach((dx, i) => {
        let line = d3.line()
            .x(function (d, i) {
                return x(d.xData)
            })
            .y(function (d, i) {
                return y(d.yData)
            });

        o.svg.append("path")
            .data([dx])
            .style("fill", "none")
            .style("stroke", colors[i])
            .style("stroke-width", "2px")
            .attr("d", line)
            .attr("data-legend", function () {
                return legend[i]
            });

    });
    // o.svg.append("g")
    //     .attr("class", "legend")
    //     .attr("transform", "translate(50,30)")
    //     .style("font-size", "12px")
    //     .call(d3.legend);

    return {xDomain: x, yDomain: y}
}