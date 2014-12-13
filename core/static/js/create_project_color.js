$(document).ready(function(){
  var $x = $('#id_color');
  $x.change(function(){
    $x.attr('style', 'background-color: ' + $x.val() + ' !important');
  });
});
