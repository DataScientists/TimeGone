$(document).ready(function(){
  var $x = $('#id_color');
  var $m = $('#modal-color');
  $('.color-selection button').click(function(e){
    var c = $(e.target).css('background-color');
    $x.val(c);
    $m.modal('hide');
  });
  $x.click(function(){
    $m.modal('show');
  });
});
