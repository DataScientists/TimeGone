$(function(){
  console.log(window.tag_autocomplete_source);
  $('#tagitTags').tagit({
    availableTags: window.tag_autocomplete_source,
    singleField: true,
    singleFieldNode: $('#id_tags'),
    allowSpaces: true
  });
  var currentTags = $("#tagitTags").tagit("assignedTags");
  if(currentTags.length==0){
    $("#tagitTags").tagit("createTag", "Health");
    $("#tagitTags").tagit("createTag", "Family");
    $("#tagitTags").tagit("createTag", "Financial");
    $("#tagitTags").tagit("createTag", "Business");
    $("#tagitTags").tagit("createTag", "Career");
    $("#tagitTags").tagit("createTag", "Intellectual");
    $("#tagitTags").tagit("createTag", "Social");
    $("#tagitTags").tagit("createTag", "Spiritual");
  }

});
