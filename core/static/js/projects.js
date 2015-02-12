"use strict";
window.addEventListener("load", function(){
  var Row = React.createClass({displayName: 'Row',
    unmount: function() {
      var node = this.getDOMNode();
      React.unmountComponentAtNode(node);
      node.parentNode.removeChild(node);
    },
    clickOk: function(e){
      e.preventDefault();
      var self = this;
      if (this.state.name && this.state.description){
        var data = {name: this.state.name,
                    description: this.state.description};
        $.post('/create/', data).success(function(x){
          var tbody = document.querySelector('table > tbody');
          var tr = document.createElement('tr');
          tr.innerHTML = '<td class="nobr"><a href="' + x + '">' + self.state.name + '</a></td><td>' +  self.state.description + '</td>';
          tbody.appendChild(tr);
          self.unmount();
        });
      }
    },
    clickRemove: function(e){
      e.preventDefault();
      this.unmount();
    },
    getInitialState: function(){
      return {
        name: '',
        description: '',
        url: ''
      };
    },
    handleNameChange: function(e){
      this.setState({name: e.target.value});
    },
    handleDescriptionChange: function(e){
      this.setState({description: e.target.value});
    },
    render: function(){
      var name = this.state.name;
      var description = this.state.description;
      return React.createElement("div", null, 
          React.createElement("input", {className: "form-control", 
        placeholder: "name", 
        value: name, onChange: this.handleNameChange}), 
          React.createElement("input", {className: "form-control", 
        placeholder: "description", 
        value: description, onChange: this.handleDescriptionChange}), 
          React.createElement("br", null), 
          React.createElement("button", {type: "button", className: "btn btn-primary", onClick: this.clickOk}, 
          React.createElement("span", {className: "glyphicon glyphicon-ok", 'aria-hidden': "true"})
          ), 
          React.createElement("button", {type: "button", className: "btn btn-default", onClick: this.clickRemove}, 
          React.createElement("span", {className: "glyphicon glyphicon-remove", 'aria-hidden': "true"})
          )
          );
    }
  });

  document.querySelector('.add-project').addEventListener("click", function(){
    var table = document.querySelector('table');
    var el = document.createElement("tr");
    table.parentNode.appendChild(el);
    React.render(React.createElement(Row, null), el);
  }, true);
}, true);
