$(function(){
  console.log(window.tag_autocomplete_source);
  $('#tagitTags').tagit({
    availableTags: window.tag_autocomplete_source,
    singleField: true,
    singleFieldNode: $('#id_tags')
  });
});
