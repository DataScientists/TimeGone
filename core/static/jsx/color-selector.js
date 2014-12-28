(function(React){

  var Color = React.createClass({
    mbchFactory: function(){
      var self = this;
      var modalButtonClickHandler = function(e){
	e.preventDefault();
	var $m = $('#modal-color');
	$('button', $m).unbind('click', modalButtonClickHandler);
	$m.modal('hide');

	var c = e.target.className.split(" ")[1];
	if (self.props.data.url){
	  $.post(self.props.data.url, {attr: 'color', abbrev: c}).success(
	    function(){
	      self.setState({abbrev: c});		    
	    }
	  );
	} else {

	  self.setState({abbrev: c});
	}
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
      return {abbrev: this.props.data.abbrev};
    },
    render: function(){
      var classes = 'color-selection ' + this.state.abbrev;
      return (
	  <button className={classes} onClick={this.handleClick}></button>
      )
    }
  });

  var x = document.querySelector('.editable-color');
  React.render(<Color data={x.dataset}/>, x);
})(React);
