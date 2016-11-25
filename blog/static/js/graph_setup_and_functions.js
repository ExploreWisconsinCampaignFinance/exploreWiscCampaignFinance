//All constant chart stuff\\
// set up the viewport, the scales, and axis generators
var time_scale;
var percent_scale;
var parseDate = d3.time.format("%Y-%m-%d").parse;
var container_dimensions = {width: 900, height: 500},
	margins = {top: 30, right: 20, bottom: 30, left: 90},
	chart_dimensions = {
		width: container_dimensions.width - margins.left - margins.right,
		height: container_dimensions.height - margins.top - margins.bottom
	};

time_scale = d3.time.scale()
	.range([0, chart_dimensions.width])
	.domain([parseDate("2012-11-07"), parseDate("2014-11-04")]);

//Change domain here
percent_scale = d3.scale.linear()
	.range([chart_dimensions.height, 0])
	.domain([100, 120000]);

var time_axis = d3.svg.axis()
	.scale(time_scale)

var count_axis = d3.svg.axis()
	.scale(percent_scale)
	.orient("left");

// draw axes
var g = d3.select('#timeseries')
  .append('svg')
	.attr("width", container_dimensions.width)
	.attr("height", container_dimensions.height)
  .append("g")
	.attr("transform", "translate(" + margins.left + "," + margins.top + ")")
	.attr("id","chart");

g.append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + chart_dimensions.height + ")")
  .call(time_axis);

g.append("g")
  .attr("class", "y axis")
  .call(count_axis);

// draw the y-axis label
d3.select('.y.axis')
	.append('text')
	.text('Money Raised')
	.attr('transform', "rotate (-90, 0, 0)")
	.attr('x', -200)
	.attr('y', -75);

function rescaleTime(bgning, nding){
	//bgning and nding are strings of the format
	//%Y-%m-%d
	time_scale.domain([parseDate(bgning), parseDate(nding)]);
	g.select(".x.axis")
		.transition().duration(1500)
		.call(time_axis);
};
		
function rescale(maxYValue) {
	percent_scale.domain([0, maxYValue])  // change scale to 0, to between 10 and 100
	g.select(".y.axis")
		.transition().duration(1500).ease("sin-in-out")  // https://github.com/mbostock/d3/wiki/Transitions#wiki-d3_ease
		.call(count_axis);  
}

var findMaxVal = function(datArray){
	var maxVal = 0;
	
	for (var i=0; i<datArray.length; i++){
		var lst = datArray[i].length
		if (typeof datArray[i][lst-1] == 'undefined'){
			continue;
		} 
		if (datArray[i][lst-1].cumulative > maxVal){				
			maxVal = datArray[i][lst-1].cumulative;
		}
	}
	return maxVal;
}
//dat is a json object, that fed into draw timeseries
var findPartyColors = function(party){
	if (party == "Democrat"){ return "#084594" }
	if (party == "Republican"){ return "#cb181d" }
	if (party == "Libertarian"){ return "#ff7f00" }
	if (party == "Independent"){ return "#a65628" }
	if (party == "WisconsinPirate"){return "#756bb1" }
}

// The graphing...
var parseDate = d3.time.format("%Y-%m-%d").parse;
function add_label(circle, d, i){
	d3.select(circle)
		.transition()
		.attr('r', 9)

	d3.select('#' + d.candidate).append('text')
		.text(d.candidate)
		.attr('text-anchor','middle')
		.style("dominant-baseline","central")
		.attr('x', time_scale(parseDate(d.date))-50)
		.attr('y', percent_scale(d.cumulative))
		.attr('class','linelabel')
		.style('opacity',0)
		.style('fill','grey')
		.transition()
			.style('opacity',1)
}

function draw_timeseries(data, id, party){
	var lineGen = d3.svg.line()
		.x(function(d){return time_scale(parseDate(d.date))})
		.y(function(d){return percent_scale(d.cumulative)})
		.interpolate("linear")

	var g = d3.select('#chart')
		.append('g')
		.attr('id', id)
		.attr('class', 'timeseries ' + id)

	g.append('path')
		.attr('d', lineGen(data))
		.attr("stroke", findPartyColors(party))

	g.selectAll('circle')
		.data(data)
		.enter()
		.append("circle")
		.attr('cx', function(d) {return time_scale(parseDate(d.date))})
		.attr('cy', function(d) {return percent_scale(d.cumulative)})
		.attr('r',0)
		.attr("fill", findPartyColors(party))

	var enter_duration = 1000;

	g.selectAll('circle')
		.transition()
		.delay(function(d, i) { return i / data.length * enter_duration; })
		.attr('r', 5)
		.each('end',function(d,i){
			if (i === data.length-1){
				add_label(this,d)
			}
		})

	g.selectAll('circle')
		.on('mouseover', function(d){
			d3.select(this)
				.transition().attr('r', 9)
		})
		.on('mouseout', function(d,i){
			if (i !== data.length-1) {
				d3.select(this).transition().attr('r', 5)
			}
		})

	g.selectAll('circle')
		.on('mouseover.tooltip', function(d){
			//console.log(d.candidate + " on")
			d3.select("text." + d.candidate).remove()
			d3.select('#chart')
				.append('text')
				.text(d.contributor + ": $" + d.amount)
				.attr('x', function() {
					if (parseDate(d.date) > parseDate("2014-04-01")) {
						return time_scale(parseDate(d.date)) - 300
					} else {
						return time_scale(parseDate(d.date)) + 10
					}
					})
					.attr('y', percent_scale(d.cumulative) - 10)
					.attr('class', d.candidate)
			})
			.on('mouseout.tooltip', function(d){
				//console.log(d.candidate + " off")
				d3.select("text." + d.candidate.replace(/ /g, "."))
					.remove()
					//.transition()
					//.duration(500)
					//.style('opacity',0)
					//.attr('transform','translate(10, -10)')
					//.remove()
			})
	}
