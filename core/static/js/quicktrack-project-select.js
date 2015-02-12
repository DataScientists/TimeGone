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

    var SelectBox = React.createClass({displayName: 'SelectBox',
        onClick: function(){
            this.props.handleClick(this);
            console.log('called');
        },
        render: function(){
            var className = "top " + this.props.color;
            var tableClassName = "quicktrack-project";
            if (this.props.selected){
                className = className + " selected";
                tableClassName = tableClassName + " selected";
            }
            return React.createElement("a", {href: "#", onClick: this.onClick}, React.createElement("table", {className: tableClassName}, 
                React.createElement("tr", null, React.createElement("td", {className: className}, " ")), 
                React.createElement("tr", null, React.createElement("td", null, "(", this.props.name, ")"))
                ));
        }
    });

    var CreateBox = React.createClass({displayName: 'CreateBox',
        render: function(){
            var className = "top " + this.props.color;
            var href = window.create_project_url + "?color=" + this.props.color + "&back=" + window.location.pathname;
            return React.createElement("a", {href: href}, React.createElement("table", {className: "quicktrack-project"}, 
                React.createElement("tr", null, React.createElement("td", {className: className}, " ")), 
                React.createElement("tr", null, React.createElement("td", null, "(   )"))
                ));
        }
    });

    var QuicktrackColorSelect = React.createClass({displayName: 'QuicktrackColorSelect',
        render: function(){
            var boxes = [];
            for (var i = 0; i<window.colored.length; i++){
                var x = window.colored[i];
                if (x[1]){
                    var selected = x[1][1] == this.props.project_id;
                    boxes.push(React.createElement(SelectBox, {color: x[0], name: x[1][0], project_id: x[1][1], key: i, selected: selected, handleClick: this.props.handleClick}));
                } else {
                    boxes.push(React.createElement(CreateBox, {color: x[0], key: i, onClick: this.handleClick}));
                }
            }
            return React.createElement("div", {id: "div_id_hours", className: "form-group"}, 
                    React.createElement("div", {className: "col-md-10 "}, 
                React.createElement("div", {className: "wrapper"}, 
                React.createElement("div", {className: "scrolls"}, 
                    boxes
            )
            )
                    )
                    );
        }
    });
    var QuicktrackContainer = React.createClass({displayName: 'QuicktrackContainer',
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
            document.getElementById('quick-track-form').action = '?pid=' + project_id;
        },
        render: function(){
            return React.createElement(QuicktrackColorSelect, {key: "1", project_id: this.state.project_id, handleClick: this.handleClick});
        }
    });
    React.render(React.createElement(QuicktrackContainer, null), target_el);
})(React);
