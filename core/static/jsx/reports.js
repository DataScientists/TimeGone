"use strict";

jQuery(function($){
  var $f = $('#filter-form');
  $('.datepicker', $f).datepicker({
    format: 'yyyy-mm-dd',
    autoclose: true
  });
});

(function(React){
  var RemoveButton = React.createClass({
    onClick: function(){
      var self = this;
      $.post(this.props.url,
             function(){
               self.props.unmount();
             });
    },
    render: function(){
      return <button className="btn btn-default" aria-label="remove" onClick={this.onClick}>
        <span className="glyphicon glyphicon-trash" aria-hidden="true"></span>
        </button>;
    }
  });
  var EditableTrackDate = React.createClass({
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
        return <span onClick={this.onClick}>{this.state.track_date}</span>;
      } else {
        var self = this;
        var el = <input type="text" onBlur={this.onBlur} onKeyDown={this.onKeyDown} value={this.state.value}/>;
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
  var EditableDescription = React.createClass({
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
        return <span onClick={this.onClick}>{this.state.description}</span>;
      } else {
        return <div>
                    <input type="text" value={this.state.description} onChange={this.onChange}/>
          <div className="btn-group" role="group">
          <button type="button" className="btn btn-default" onClick={this.saveEdit}>
          <span className="glyphicon glyphicon-ok" aria-hidden="true"></span>
          </button>
          <button type="button" className="btn btn-default" onClick={this.cancelEdit}>
          <span className="glyphicon glyphicon-remove" aria-hidden="true"></span>
          </button>
          </div>
          </div>;
      }
    }
  });
  var EditableHours = React.createClass({
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
        return <span onClick={this.onClick}>{this.state.hours}</span>;
      } else {
        return <div>
          <input type="text" value={this.state.hours} onChange={this.onChange}/>
          <div className="btn-group" role="group">
          <button type="button" className="btn btn-default" onClick={this.saveEdit}>
          <span className="glyphicon glyphicon-ok" aria-hidden="true"></span>
          </button>
          <button type="button" className="btn btn-default" onClick={this.cancelEdit}>
          <span className="glyphicon glyphicon-remove" aria-hidden="true"></span>
          </button>
          </div>
          </div>;
      }
    }
  });
  var EditableProject = React.createClass({
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
        return <span onClick={this.onClick}>{this.state.name}</span>;
      } else {
        var options = [];
        options = this.props.projects.map(function(x){
          return <option value={x[0]}>{x[1]}</option>;
        });
        return <div>
          <select ref="menu" onChange={this.onChange} value={this.state.pk}>{options}</select>
          <div className="btn-group" role="group">
          <button type="button" className="btn btn-default" onClick={this.saveEdit}>
          <span className="glyphicon glyphicon-ok" aria-hidden="true"></span>
          </button>
          <button type="button" className="btn btn-default" onClick={this.cancelEdit}>
          <span className="glyphicon glyphicon-remove" aria-hidden="true"></span>
          </button>
          </div>
          </div>;
      }
    }
  });
  var Row = React.createClass({
    render: function(){
      return <tr>
        <td><EditableProject url={this.props.data.project_url}
      name={this.props.data.project_name}
      pk={this.props.data.project_pk}
      projects={this.props.data.projects}/></td>
        <td><EditableHours hours={this.props.data.hours} url={this.props.data.hours_url}/></td>
        <td><EditableDescription description={this.props.data.description} url={this.props.data.description_url}/></td>
        <td><EditableTrackDate track_date={this.props.data.track_date} url={this.props.data.track_date_url} unmount={this.unmount}/></td>
        <td><RemoveButton unmount={this.unmount} url={this.props.data.delete_url}/></td>
      </tr>;
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
                React.render(<Row data={JSON.parse(x.dataset.props)} el={x}/>, x);
              });
})(React);
