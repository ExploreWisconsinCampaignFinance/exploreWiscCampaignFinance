$("#sel_district").change(function() {
	var cont_data = [];
	var maxVal = 0;
	if ($(this).val() == "Select a District") {return }
	//Remember to remove the previous graph		
	$('.timeseries.drawnTimeSeries').remove();
	$('.key_line').remove();
	
	var distNum = $(this).val();
	//constructing the data for the legend
	var leg_data = [];
	
	//Go through each candidate who ran
	//	searching for the matching district 
	$.each(cand_data, function(i, fb) {
		if (fb.district != distNum){
			return;
		}
		console.log(fb.candidate)
		if (fb.candidate == "None, None"){ 
			return; 
		}
		//Collect campaign data for who won, party, etc
		var splt = fb.candidate.split(",");
		var obj = {};
		//Break into key name and display name
		obj["line_id"] = fb.candidate;
		obj["line_name"] = splt[splt.length-1] + " " + splt[0];
		obj["party"] = fb.party.replace(" ", "");
		obj["won"] = fb.won;
		leg_data.push(obj);
	})
	//Collect contributor data from url and store it
	for (var i=0; i<leg_data.length; i++){
		var cand_name = leg_data[i].line_id
		var theurl = "/contributor_data/" + cand_name + "/" + year;
		console.log("The url for contrib data: " + theurl);
		var jsonOutData;
		
		var ajaxOpts = {
			async: false,
			dataType: "json",
			success: function(data) { jsonOutData = data; }
		};
		
		$.ajax(theurl, ajaxOpts);
		cont_data.push(jsonOutData)
	}
	console.log("Max val is " + findMaxVal(cont_data));

	rescale(findMaxVal(cont_data))
	for (var i=0; i<leg_data.length; i++){
	
		draw_timeseries(cont_data[i], 'drawnTimeSeries', leg_data[i].party)
	
	}
	// drawing the key
	var key_items = d3.select('#key')
	  .selectAll('div')
	  .data(leg_data)
	  .enter()
	  .append('div')
		.attr('class','key_line')
		.attr('id',function(d){return d.line_id+"_key"})

	key_items.append('div')
		.attr('id', function(d){return 'key_square_' + d.line_id})
		.attr('class', function(d){return 'key_square ' + d.line_id + " " + d.party})
	//Marking winner
	key_items.append('div')
		.attr('class','key_label')
		.text(function(d){
			if (d.won == 1){
				return d.line_name + "*"
			} else {
				return d.line_name
			}
		})

})
