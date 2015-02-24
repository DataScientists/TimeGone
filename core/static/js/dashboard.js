"use strict";

function update_bigtime_href(s){
    var a = document.getElementById('bigtime');
    a.href = a.href.replace(/(\/[^\/]*)$/, s);
}

function sum_hours(data){
  var hours = 0;
  for (var i = 0; i < data.length; i++){
    hours = hours + data[i].hours;
  }
  return hours;
}

function draw_graph(data){
  var HOUR_HEIGHT = 15;
  var HOR_OFFSET = 15;
  var c = document.getElementById('graph');
  c.width = 180;
  var hours = Math.max(24, sum_hours(data));
  c.height = HOUR_HEIGHT * hours;
  var w = c.width;
  var h = c.height;
  var ctx = c.getContext('2d');
  ctx.font = "10px Arial";
  ctx.fillStyle = '#000000';
  ctx.clearRect(0, 0, w, h);
  ctx.save();
  ctx.rotate(-Math.PI/2);
  for (var i = 0; i < hours; i++){
    if (i == 24){
      ctx.fillStyle = '#ff0000';
    }
    ctx.fillText('|', - h + i * HOUR_HEIGHT, 10);
  }
  ctx.restore();
  var base = 0;
  for (var i = 0; i < data.length; i++){
    var x = data[i];
    ctx.fillStyle = x['project__color'];
    var height = x['hours'] * HOUR_HEIGHT;
    ctx.fillRect(HOR_OFFSET, h - (base + height), w - HOR_OFFSET, height);
    ctx.strokeRect(HOR_OFFSET, h - (base + height), w - HOR_OFFSET, height);
    base = base + height;
  }
}

function draw_legend(data){
  var i;

  var seen = {};
  var data_to_draw = [];
  for (i = 0; i < data.length; i++){
    var project_name = data[i]['project__name'];
    if (seen[project_name] == undefined){
      seen[project_name] = 1;
      data_to_draw.push([project_name, data[i]['project__color']]);
    }; 
  }

  var c = document.getElementById('legend');
  var w = c.width;
  var h = c.height;
  var ctx = c.getContext('2d');
  ctx.clearRect(0, 0, w, h);

  var offset_y = 25;
  var offset_x = 10;

  ctx.font = "10px Arial";
  ctx.fillStyle = '#000000';
  for (i = 0; i < data_to_draw.length; i++){
    ctx.fillText(data_to_draw[i][0], offset_x + 30, offset_y + 25 * i);
  }

  for (i = 0; i < data_to_draw.length; i++){
    ctx.fillStyle = data_to_draw[i][1];
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
