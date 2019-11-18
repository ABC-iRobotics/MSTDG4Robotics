import React from 'react';
import FormField from './FormField';
import FormTitle from './FormTitle';
class Form extends React.Component {
    constructor(props){
        super(props);
        this.state = this.props.params;
    }
    onSubmitHandler = event => {
        event.preventDefault();

        this.props.onSubmitHandler(this.state);
    }

    handleChange = (fieldName, fieldValue) => {
        this.setState({[fieldName]: fieldValue});
    }
    
    render() {
        return (
           
            
                <div className="ui middle aligned center aligned grid">
                    <div className="column">
                        <FormTitle title={this.state.title}/>
                        <form className="ui large form" onSubmit={this.onSubmitHandler}>
                            <div>
                                <FormField label="V-REP path" handleChange={this.handleChange} fieldName="vrepPath" fieldValue="" iconClass="file" fieldPlaceholder="V-REP application name" fieldType="text"/>
                                <FormField label="Selected mesh" handleChange={this.handleChange} fieldName="meshPath" fieldValue="" iconClass="file" fieldPlaceholder="Mesh path" fieldType="file"/>
                                <FormField handleChange={this.handleChange} fieldName="datasetCount" fieldValue="" iconClass="sort numeric up" fieldPlaceholder="Dataset size" fieldType="number"/>
                                <FormField handleChange={this.handleChange} fieldName="meshCount" fieldValue="" iconClass="sort numeric up" fieldPlaceholder="Count of meshes" fieldType="number"/>
                                
                                <button type="submit" className="ui button">Submit</button>
                            </div>

                            <div className="ui error message"></div>

                        </form>

                    </div>
                </div>
        
        );
    }
}
export default Form;