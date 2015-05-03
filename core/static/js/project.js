"use strict";
(function(React){
  var Div = React.createClass({displayName: 'Div',
    handleClick: function(){
      this.props.handle(true, this.state.text);
    },
    getInitialState: function() {
      return {text: this.props.text};
    },
    render: function(){
      return React.createElement("div", {onClick: this.handleClick}, this.props.text);
    }
  });

  var Form = React.createClass({displayName: 'Form',
    handleSubmit: function(e){
      e.preventDefault();
      var self = this;
      $.post(this.props.data.url,
    	     {'attr': this.props.data.attr,
    	      'text': this.state.text}).success(function(){
    		self.props.handle(false, self.state.text);
    	      }).error(function(){
    		console.error('failed');
    	      });

    },
    handleBlur: function(e){
      this.handleSubmit(e);
    },
    handleChange: function(e){
      this.setState({'text': e.target.value});
    },
    getInitialState: function() {
      return {text: this.props.text};
    },
    componentDidMount: function(){
      this.setState({'initial_text': this.state.text});
      this.refs.textInput.getDOMNode().focus();
    },
    render: function(){
      return (
  	  React.createElement("form", {onSubmit: this.handleSubmit}, 
  	  React.createElement("input", {type: "text", ref: "textInput", value: this.state.text, onBlur: this.handleBlur, onChange: this.handleChange})
	  )
      );
    }
  });

  var Editable = React.createClass({displayName: 'Editable',
    handleEditify: function(editable, text){
      this.setState({'editable': editable, 'text': text});
    },
    getInitialState: function() {
      return {editable: false, text: this.props.text};
    },
    render: function(){
      if (this.state.editable){
	return (
	    React.createElement(Form, {data: this.props.data, text: this.state.text, handle: this.handleEditify})
	);
      } else {
	return (
	    React.createElement(Div, {text: this.state.text, handle: this.handleEditify})
	);
      }
    }
  });

  var els = document.querySelectorAll('.click-editable');
  for (var i = 0; i < els.length; i++){
    var x = els[i];
    React.render(
	React.createElement(Editable, {data: x.dataset, text: x.textContent}),
      x
    );
  }
})(React);
