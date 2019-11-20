import React from 'react';

class FormTitle extends React.Component {
  render() {
    return (
        <h2 className="ui teal image header">
        <div className="content">
            {this.props.title}
        </div>
        </h2>
    );
  }
}
export default FormTitle;