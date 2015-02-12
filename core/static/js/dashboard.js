"use strict";

function update_bigtime_href(s){
    var a = document.getElementById('bigtime');
    a.href = a.href.replace(/(\/[^\/]*)$/, s);
}

function draw_graph(data){
  var c = document.getElementById('graph');
  var w = c.width;
  var h = c.height;
  var ctx = c.getContext('2d');
  ctx.font = "10px Arial";
  ctx.fillStyle = '#000000';
  ctx.clearRect(0, 0, w, h);
  ctx.save();
  ctx.rotate(-Math.PI/2);
  for (var i = 0; i < 24; i++){
    ctx.fillText('|', - h + i * (h/24), 10);
  }
  ctx.restore();
  var base = 0;
  for (var i = 0; i < data.length; i++){
    var x = data[i];
    ctx.fillStyle = x['project__color'];
    var height = (x['hours'] / 24) * h;
    ctx.fillRect(15, h - (base + height), w - 15, height);
    ctx.strokeRect(15, h - (base + height), w - 15, height);
    base = base + height;
  }
}
function draw_legend(data){
  var c = document.getElementById('legend');
  var w = c.width;
  var h = c.height;
  var ctx = c.getContext('2d');
  ctx.clearRect(0, 0, w, h);
  var offset_y = 25;
  var offset_x = 10;

  ctx.font = "10px Arial";
  ctx.fillStyle = '#000000';
  for (var i = 0; i < data.length; i++){
    var x = data[i];
    ctx.fillText(x['project__name'], offset_x + 30, offset_y + 25 * i);
  }

  for (var i = 0; i < data.length; i++){
    var x = data[i];
    ctx.fillStyle = x['project__color'];
    ctx.fillRect(offset_x, offset_y + 25 * i - 12 , 20, 20);
  }  
}
function draw(data){
  draw_graph(data);
  draw_legend(data);
}
$(document).ready(function(){
  var $x = $('#dates');
  $x.change(function(){
    var date = $x.val();
    var settings = {
      'data': {'date': date},
      'async': false,
      'dataType': 'json',
      'success': function(data){
	draw(data.g);
        var s = (date == window.today_date) ? '/' : ('/?date=' + date);
	window.history.pushState({}, window.document.title, s);
        update_bigtime_href(s);
      }
    };
    $.ajax(settings);
  });
  draw(window.graph);
  $('.flip-container').click(function(){
    $('.flip-container').toggleClass('flip');
  });
});
