var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 1100 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

// Append svg to div
var svg = d3.select("#lineChart")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");


function d3lineChart(dataset) {

  var dataset = dataset.map(function (d) {
    return {...d, time: d.time * 1000};
    }) ;

  // group data by topic name i.e. sport
  var sumstat = d3.nest()
    .key(function(d) { return d.topic_name;})
    .entries(dataset);

  // X axis
  var x = d3.scaleTime()
    .domain(d3.extent(dataset, function(d) { return new Date(d.time); }))
    .range([ 0, width ]);
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

  // Y axis
  var y = d3.scaleLinear()
    .domain([0, d3.max(dataset, function(d) { return +d.value; })])
    .range([ height, 0 ]);
  svg.append("g")
    .call(d3.axisLeft(y));

  // Render colours per topic_name
  var res = sumstat.map(function(d){ return d.key })
  var colour = d3.scaleOrdinal()
    .domain(res)
    .range(['#e41a1c','#377eb8','#4daf4a'])

  // Draw
  svg.selectAll(".line")
      .data(sumstat)
      .enter()
      .append("path")
        .attr("fill", "none")
        .attr("stroke", function(d){ return colour(d.key) })
        .attr("stroke-width", 2.5)
        .attr("d", function(d){
          return d3.line()
            .x(function(d) { return x(d.time); })
            .y(function(d) { return y(+d.value); })
            (d.values)
        })

}