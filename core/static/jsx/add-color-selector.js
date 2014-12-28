(function(React){
  var Color = React.createClass({
    mbchFactory: function(){
      var self = this;
      var modalButtonClickHandler = function(e){
	e.preventDefault();
	var $m = $('#modal-color');
	$('button', $m).unbind('click', modalButtonClickHandler);
	$m.modal('hide');
	var color = e.target.className.split(" ")[1];
	self.setState({abbrev: color});		    
      }
      return modalButtonClickHandler;
    },
    handleClick: function(e){
      e.preventDefault();
      var $m = $('#modal-color');
      $('button', $m).click(this.mbchFactory());
      $m.modal('show');
    },
    getInitialState: function(){
      if (this.props.data.abbrev){
	return {abbrev: this.props.data.abbrev};
      } else {
	return {abbrev: ''};
      }
    },
    render: function(){
      var classes = 'color-selection ' + this.state.abbrev;
      return (
	  <div>
	  <button className={classes} onClick={this.handleClick}></button>
	  <input type="hidden" name="color" value={this.state.abbrev}/>
	  </div>
      )
    }
  });

  var x = document.querySelector('.editable-color');
  React.render(<Color data={x.dataset}/>, x);
})(React);

jQuery(function($){
  var $f = $('form');
  $f.submit(function(e){
    if (!$('[name=color]', $f).val()){
      e.preventDefault();
      modal_alert('Choose color', 'Project must have some color assigned to it. It can not stay white.');
    }
  });
});
