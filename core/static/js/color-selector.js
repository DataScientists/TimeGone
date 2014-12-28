(function(React){

  var Color = React.createClass({displayName: 'Color',
    mbchFactory: function(){
      var self = this;
      var modalButtonClickHandler = function(e){
	e.preventDefault();
	console.log('seen');
	var $m = $('#modal-color');
	$('button', $m).unbind('click', modalButtonClickHandler);
	$m.modal('hide');

	var c = e.target.className.split(" ")[1];
	if (self.props.data.url){
	  console.log('sayed a');
	  $.post(self.props.data.url, {attr: 'color', abbrev: c}).success(
	    function(){
	      console.log('sayed b');
	      console.log('bew c', c);
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
      console.log('set, show');
    },
    getInitialState: function(){
      console.log('props', this.props);
      return {abbrev: this.props.data.abbrev};
    },
    render: function(){
      var classes = 'color-selection ' + this.state.abbrev;
      return (
	  React.createElement("button", {className: classes, onClick: this.handleClick})
      )
    }
  });

  var x = document.querySelector('.editable-color');
  React.render(React.createElement(Color, {data: x.dataset}), x);
})(React);
