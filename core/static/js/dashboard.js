function draw(data){
    console.log(data);
    var c = document.getElementById('graph');
    var w = c.width;
    var h = c.height;
    var ctx = c.getContext('2d');
    ctx.font = "10px Arial";
    ctx.fillStyle = '#000000';
    ctx.clearRect(0, 0, w, h);
    ctx.save()
    ctx.rotate(-Math.PI/2)
    for (var i = 0; i < 24; i++){
	ctx.fillText(i, - h + i * (h/24), 10);
    }
    ctx.restore()
    var base = 0;
    // from http://ios7colors.com
    var colors = ['#FF9500', '#FF3B30', 
		  '#4CD964', '#FFCC00', '#BDBEC2', '#1F1F21',
		  '#FF2D55', '#5856D6', '#007AFF', '#34AADC'];
    for (var i = 0; i < data.length; i++){
	ctx.fillStyle = colors[i];
	height = (data[i]['hours'] / 24) * h;
	console.log(i, height);
	ctx.fillRect(15, h - (base + height), w - 15, height);
	ctx.strokeRect(15, h - (base + height), w - 15, height);
	base = base + height;
    }
    
}
$(document).ready(function(){
    var $x = $('#dates');
    $x.change(function(){
	var settings = {
	    'data': {'date': $x.val()},
	    'async': false,
	    'dataType': 'json',
	    'success': function(data){
		console.log(data);
		console.log(data.g);
		draw(data.g);
	    }
	};
	console.log(settings);
	$.ajax(settings);
    });
    draw(graph);
});
