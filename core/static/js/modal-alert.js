function modal_alert(t, d){
  $m = $('#modal-alert');
  $('.modal-title', $m).text(t);
  $('.modal-body > p', $m).text(d);
  $m.modal('show');
}
