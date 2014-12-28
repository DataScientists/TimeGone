jQuery(function($){
  var $f = $('#filter-form');
  
  $('.datepicker', $f).datepicker({
    format: 'yyyy-mm-dd',
    autoclose: true
  });

});
