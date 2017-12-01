$(function() {
    let s = '#svg-wrapper';
    let o = initSvg(s, $(s).width(), 300);
    drawTest(o);
});


function drawTest(o) {

    let data = [[0,10], [10, 20], [20, 30], [30, 20], [40, 0], [50, 0], [60, 0]];
    let data2 = [{x: 0, y: 10}, {x: 10, y: 20}, {x: 20, y: 30}, {x: 30, y: 20}, {x: 40, y: 0}];
    let data3 = [{x: -10, y: 30}, {x: 5, y: 10}, {x: 10, y: 50}, {x: 15, y: 30}, {x: 20, y: 0}];

    let x = o.x.domain(d3.extent(data2, function(d) { return d.x; }));
    let y = o.y.domain([0, d3.max(data2, function (d) { return d.y; })]);

    let area = d3.area()
        .x(function(d) { return x(d.x) })
        .y0(o.height)
        .y1(function(d) { return y(d.y); });

    o.svg.selectAll('.area')
        .data([data2, data3])
        .enter().append('path')
        .style('fill', 'lightsteelblue')
        .attr('class', 'area')
        .attr('d', area)

}
