import React from 'react';
import FormField from './FormField';
import FormFieldSelect from './FormFieldSelect';
import FormTitle from './FormTitle';


class Form extends React.Component {
    constructor(props){
        super(props);

        this.state = this.props.params;
        this.state.selectedTask = this.getTask();
    }
    onSubmitHandler = event => {
        event.preventDefault();
        var saveObject = {
            base: {
                taskName: this.state.selectedTask.taskName,
                vrepPath: this.state.model.vrepPath
            },
            inputs: this.state.model.inputs.concat(this.state.selectedTask.inputs).map(x => {
                return {name: x.fieldName, value: x.fieldValue, type: x.fieldType}
            })
        }
        this.props.onSubmitHandler(saveObject);
    }

    handleChange = (fieldName, fieldValue) => {
        var model = this.state.model;
        var item = model.inputs.find(x => x.fieldName === fieldName);
        if(item) {
            item.fieldValue = fieldValue;
            this.setState({model: model});
        } 
        else {
            item = model.tasks.find(x => x.task.taskName === this.state.selectedTask.taskName).task.inputs.find(y => y.fieldName === fieldName);
            if(item){
                item.fieldValue = fieldValue;
                this.setState({model: model});
            }
            else {
                this.setState({[fieldName]: fieldValue});
            }
        }
    }

    handleDropDownChange = (event, item) =>{
        this.getTask(item.value);
    }
    
    getTask = (taskName) => {
        var task = {};
        if(taskName){
            task = this.state.model.tasks.find(x => {
                return x.task.taskName === taskName;
            });
            this.setState({selectedTask: task.task, isTaskSelected: true});
         }
        if(!taskName && this.state.model && this.state.model.tasks.length > 0) {
            task = this.state.model.tasks[0];
            return task.task;
        }
    }

    render() {
        return (
                <div className="ui middle aligned center aligned grid">
                    <div className="column">
                        <FormTitle title={this.state.model.title}/>
                   
                        <form className="ui large form" onSubmit={this.onSubmitHandler}>
                        <hr/>
                            <div className="base-details">
                                <div>
                                    <h3>
                                        <label>{this.state.title}</label>
                                    </h3>
                                    <hr/>
                                </div>
                               {
                                this.state.model.inputs.map(x =>{
                                    return <FormField key={x.fieldName} label={x.label} handleChange={this.handleChange} fieldName={x.fieldName} fieldValue={x.fieldValue?x.fieldValue: undefined} iconClass={x.iconClass} fieldPlaceholder={x.fieldPlaceholder} fieldType={x.fieldType}/>
                                })
                               }
                            </div>
                            <div> 
                            <FormFieldSelect params={this.state} handleDropDownChange={this.handleDropDownChange}/>
                            </div>
                            <div className="task-details" hidden={!this.state.isTaskSelected}>
                            <hr/>
                            <div>
                                <h3>
                                    <label>{this.state.selectedTask.label}</label>
                                </h3>
                                <hr/>
                            </div>
                                {
                                    this.state.selectedTask.inputs.map(x =>{
                                        return <FormField key={x.fieldName} label={x.label} handleChange={this.handleChange} fieldName={x.fieldName} fieldValue={x.fieldValue?x.fieldValue: undefined} iconClass={x.iconClass} fieldPlaceholder={x.fieldPlaceholder} fieldType={x.fieldType}/>                                        })
                                }
                            </div>

                            <button type="submit" disabled={!this.state.isTaskSelected} className="ui button">Submit</button>
                            <div className="ui error message"></div>
                        </form>
                    </div>
                </div>
        );
    }
}
export default Form;