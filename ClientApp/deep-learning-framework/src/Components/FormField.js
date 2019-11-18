import React from 'react';

class FormField extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      value: props.value
    }
  }
  
  handleChange = (evt) =>{
    this.props.handleChange(evt.target.name, evt.target.value);
  }

  render() {
    return (
      <div className="field">
        <div className="ui left icon input">
            <i className={this.props.iconClass+" icon"}></i>
            <input id={this.props.fieldName} name={this.props.fieldName} type={this.props.fieldType} onChange={this.handleChange} className="form-control form-control-file" placeholder={this.props.fieldPlaceholder} value={this.state.value}/>
        </div>
      </div>
    );
  }
}
export default FormField;