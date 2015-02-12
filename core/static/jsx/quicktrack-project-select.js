"use strict";

var pid = (function(){
  var r = /pid=(\d+)/;
  var m = r.exec(location.search);
  if (m){
    return m[1];
  } else {
    return false;
  }
})();

(function(React){
  var project_el = document.getElementById('id_project');
  var target_el = document.createElement('div');
  target_el.setAttribute('id', 'quicktrack-project-select');
  project_el.parentNode.insertBefore(target_el, project_el);
  
  var SelectBox = React.createClass({
    onClick: function(){
      this.props.handleClick(this);
    },
    render: function(){
      var className = "top " + this.props.color;
      var tableClassName = "quicktrack-project";
      if (this.props.selected){
        className = className + " selected";
        tableClassName = tableClassName + " selected";
      }
      return <a href="#" onClick={this.onClick}><table className={tableClassName}>
        <tr><td className={className}> </td></tr>
        <tr><td>({this.props.name})</td></tr>
        </table></a>;
    }
  });

  var CreateBox = React.createClass({
    render: function(){
      var className = "top " + this.props.color;
      var href = window.create_project_url + "?color=" + this.props.color + "&back=" + window.location.pathname;
      return <a href={href}><table className="quicktrack-project">
        <tr><td className={className}> </td></tr>
        <tr><td>(&nbsp;&nbsp;&nbsp;)</td></tr>
        </table></a>;
    }
  });

  var QuicktrackColorSelect = React.createClass({
    render: function(){
      var boxes = [];
      for (var i = 0; i<window.colored.length; i++){
        var x = window.colored[i];
        if (x[1]){
          var selected = x[1][1] == this.props.project_id;
          boxes.push(<SelectBox color={x[0]} name={x[1][0]} project_id={x[1][1]} key={i} selected={selected} handleClick={this.props.handleClick}/>);
        } else {
          boxes.push(<CreateBox color={x[0]} key={i} onClick={this.handleClick}/>);
        }
      }
      return <div id="div_id_hours" className="form-group">
        <div className="col-md-10 ">
        <div className="wrapper">
        <div className="scrolls">
        {boxes}
      </div>
        </div>
        </div>
        </div>;
    }
  });

  var QuicktrackContainer = React.createClass({
    getInitialState: function(){
      if (pid){
        return {project_id: pid};
      } else {
        return {project_id: false};
      }
    },
    handleClick: function(childComponent){
      var project_id = childComponent.props.project_id;
      this.setState({'project_id': project_id});
      document.getElementById('id_project').value = project_id;
      var f = document.getElementById('quick-track-form');
      var u = new Url(f.action);
      u.query.pid = project_id;
      f.action = u.toString();
    },
    render: function(){
      return <QuicktrackColorSelect key="1" project_id={this.state.project_id} handleClick={this.handleClick}/>;
    }
  });
  React.render(<QuicktrackContainer/>, target_el);
})(React);
