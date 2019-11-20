import React from 'react';
import logo from '../logo.png';

class Title extends React.Component {
  render() {
    return (
        <div className="logo-container btm">
          <img className="ui centered small image" src={logo} alt="Logo"/>
        </div>
    );
  }
}
export default Title;