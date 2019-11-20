import React from 'react';
import { Dropdown } from 'semantic-ui-react';

class FormFieldSelect extends React.Component {
  render() {
    var list = this.props.params.model.tasks.map(x =>
        {
            return{
                key: x.task.taskName,
                value: x.task.taskName,
                text: x.task.label
            };
        }
    );

    return (
        <div className="field">
            <label>Select a task</label>
            <Dropdown placeholder='Select Task' fluid selection onChange={this.props.handleDropDownChange} options={list}/>     
        </div>
    );
  }
}
export default FormFieldSelect;