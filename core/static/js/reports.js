"use strict";

jQuery(function($){
  var $f = $('#filter-form');
  $('.datepicker', $f).datepicker({
    format: 'yyyy-mm-dd',
    autoclose: true
  });
});

(function(React){
  var RemoveButton = React.createClass({displayName: 'RemoveButton',
    onClick: function(){
      var self = this;
      $.post(this.props.url,
             function(){
               self.props.unmount();
             });
    },
    render: function(){
      return React.createElement("button", {className: "btn btn-default", 'aria-label': "remove", onClick: this.onClick}, 
        React.createElement("span", {className: "glyphicon glyphicon-trash", 'aria-hidden': "true"})
        );
    }
  });
  var EditableTrackDate = React.createClass({displayName: 'EditableTrackDate',
    getInitialState: function(){
      return {
        'state': 'view',
        'track_date': this.props.track_date
      };
    },
    onClick: function(){
      this.setState({'state': 'edit'});
    },
    onBlur: function(){
      this.setState({'state': 'view'});
    },
    onKeyDown: function(evt){
      if (evt.keyCode == 13 || evt.keyCode == 27){
        this.setState({'state': 'view'});
      }
    },
    render: function(){
      if (this.state.state == 'view'){
        return React.createElement("span", {onClick: this.onClick}, this.state.track_date);
      } else {
        var self = this;
        var el = React.createElement("input", {type: "text", onBlur: this.onBlur, onKeyDown: this.onKeyDown, value: this.state.value});
        window.setTimeout(function(){
          var node = el._owner.getDOMNode();
          $(node).datepicker({
            format: 'yyyy-mm-dd',
            autoclose: true
          }).focus().on('changeDate', function(evt){
            self.setState({'track_date': new_date,
                           'state': 'view'});
            $(node).datepicker('remove');
            var new_date = evt.format();
            $.post(self.props.url, {track_date: new_date});
            var filter_start_date = $('input[name=start]').val();
            var filter_end_date = $('input[name=end]').val();
            var in_filtered_range = (filter_start_date <= new_date) && (new_date <= filter_end_date);
            if (! in_filtered_range){ 
              self.props.unmount();
            }
          });
        }, 0);
        return el;
      }
    }
  });

  var EditableCreatedAt = React.createClass({displayName: 'EditableTrackDate',
    getInitialState: function(){
      return {
        'state': 'view',
        'created_at': this.props.created_at
      };
    },
    render: function(){
      if (this.state.state == 'view'){
        return React.createElement("span", {onClick: this.onClick}, this.state.created_at);
      }
    }
  });

  var EditableDescription = React.createClass({displayName: 'EditableDescription',
    getInitialState: function(){
      return {
        'description': this.props.description,
        'state': 'view'
      };
    },
    onClick: function(){
      this.setState({'state': 'edit'});
    },
    saveEdit: function(){
      $.post(this.props.url, {description: this.state.description});
      this.setState({'state': 'view'});
    },
    cancelEdit: function(){
      this.setState({'state': 'view'});
    },
    onChange: function(event){
      this.setState({'description': event.target.value});
    },
    render: function(){
      if (this.state.state == 'view'){
        return React.createElement("span", {onClick: this.onClick}, this.state.description);
      } else {
        return React.createElement("div", null, 
                    React.createElement("input", {type: "text", value: this.state.description, onChange: this.onChange}), 
          React.createElement("div", {className: "btn-group", role: "group"}, 
          React.createElement("button", {type: "button", className: "btn btn-default", onClick: this.saveEdit}, 
          React.createElement("span", {className: "glyphicon glyphicon-ok", 'aria-hidden': "true"})
          ), 
          React.createElement("button", {type: "button", className: "btn btn-default", onClick: this.cancelEdit}, 
          React.createElement("span", {className: "glyphicon glyphicon-remove", 'aria-hidden': "true"})
          )
          )
          );
      }
    }
  });
  var EditableHours = React.createClass({displayName: 'EditableHours',
    getInitialState: function(){
      return {
        'state': 'view',
        'hours': this.props.hours
      };
    },
    saveEdit: function(){
      $.post(this.props.url, {hours: this.state.hours});
      this.setState({'state': 'view'});
    },
    cancelEdit: function(){
      this.setState({'state': 'view'});
    },
    onClick: function(){
      this.setState({'state': 'edit'});
    },
    onChange: function(event){
      this.setState({'hours': event.target.value});
    },
    render: function(){
      if (this.state.state == 'view'){
        return React.createElement("span", {onClick: this.onClick}, this.state.hours);
      } else {
        return React.createElement("div", null, 
          React.createElement("input", {type: "text", value: this.state.hours, onChange: this.onChange}), 
          React.createElement("div", {className: "btn-group", role: "group"}, 
          React.createElement("button", {type: "button", className: "btn btn-default", onClick: this.saveEdit}, 
          React.createElement("span", {className: "glyphicon glyphicon-ok", 'aria-hidden': "true"})
          ), 
          React.createElement("button", {type: "button", className: "btn btn-default", onClick: this.cancelEdit}, 
          React.createElement("span", {className: "glyphicon glyphicon-remove", 'aria-hidden': "true"})
          )
          )
          );
      }
    }
  });
  var EditableProject = React.createClass({displayName: 'EditableProject',
    getInitialState: function(){
      var mapping = {};
      for (var i = 0; i < this.props.projects.length; i++){
        var x = this.props.projects[i];
        mapping[x[0]] = x[1];
      }
      return {
        'state': 'view',
        'name': this.props.name,
        'pk': this.props.pk,
        'mapping': mapping
      };
    },
    onClick: function(){
      this.setState({'state': 'edit'});
    },
    saveEdit: function(){
      var self = this;
      $.post(this.props.url, {'pk': this.state.pk});
      this.setState({'state': 'view',
                     'name': this.state.mapping[this.state.pk]});
    },
    cancelEdit: function(){
      this.setState({'state': 'view'});
    },
    onChange: function(e){
      this.setState({'pk': this.refs.menu.getDOMNode().value});
    },
    render: function(){
      if (this.state.state == 'view'){
        return React.createElement("span", {onClick: this.onClick}, this.state.name);
      } else {
        var options = [];
        options = this.props.projects.map(function(x){
          return React.createElement("option", {value: x[0]}, x[1]);
        });
        return React.createElement("div", null, 
          React.createElement("select", {ref: "menu", onChange: this.onChange, value: this.state.pk}, options), 
          React.createElement("div", {className: "btn-group", role: "group"}, 
          React.createElement("button", {type: "button", className: "btn btn-default", onClick: this.saveEdit}, 
          React.createElement("span", {className: "glyphicon glyphicon-ok", 'aria-hidden': "true"})
          ), 
          React.createElement("button", {type: "button", className: "btn btn-default", onClick: this.cancelEdit}, 
          React.createElement("span", {className: "glyphicon glyphicon-remove", 'aria-hidden': "true"})
          )
          )
          );
      }
    }
  });
  var Row = React.createClass({displayName: 'Row',
    render: function(){
      return React.createElement("tr", null, 
        React.createElement("td", null, React.createElement(EditableProject, {url: this.props.data.project_url, 
      name: this.props.data.project_name, 
      pk: this.props.data.project_pk, 
      projects: this.props.data.projects})), 
        React.createElement("td", null, React.createElement(EditableHours, {hours: this.props.data.hours, url: this.props.data.hours_url})), 
        React.createElement("td", null, React.createElement(EditableDescription, {description: this.props.data.description, url: this.props.data.description_url})), 
        React.createElement("td", null, React.createElement(EditableTrackDate, {track_date: this.props.data.track_date, url: this.props.data.track_date_url, unmount: this.unmount})), 
        React.createElement("td", null, React.createElement(EditableCreatedAt, {created_at: this.props.data.created_at, url: this.props.data.created_at_url, unmount: this.unmount})),
        React.createElement("td", null, React.createElement(RemoveButton, {unmount: this.unmount, url: this.props.data.delete_url}))
      );
    },
    unmount: function() {
      try { // when child component plays with datepicker getting node breaks
        var node = this.getDOMNode();
        React.unmountComponentAtNode(node);        
      } catch(e){};
      $(this.props.el).remove();
    }
  });
  [].map.call(document.querySelectorAll('.editable-inplace'), 
              function(x){
                React.render(React.createElement(Row, {data: JSON.parse(x.dataset.props), el: x}), x);
              });
})(React);
