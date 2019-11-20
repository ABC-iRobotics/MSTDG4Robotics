import React from 'react';
import './App.css';
import Form from "./Components/Form";
import Title from "./Components/Title";
import { Dimmer, Loader } from 'semantic-ui-react';

const {ipcRenderer} = window.require('electron');

class App extends React.Component {
  constructor(props) {
    super(props);
    var model = this.handleInitData(ipcRenderer.sendSync('get-init-data', ""));
    this.state = {
      vrepPath: "",
      meshCount: 0,
      datasetCount: 0,
      title: "Base Details",
      isLoading: false, 
      selectedTask: {},
      isTaskSelected: false,
      model: model
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleInitData = this.handleInitData.bind(this);
  }

  handleInitData(args){
    return args;
  }
  pathConverter(path){
    if(path && path.length > 0){
      return path.substring(path.lastIndexOf("\\")+1);
    }
    return "";
  }
  handleSubmit(params) {
    this.setState({isLoading: true});
    
    for (let i = 0; i < params.inputs.length; i++) {
      const element = params.inputs[i];
      if(element.type === "file"){
        element.value = this.pathConverter(element.value);
      }
    }

    ipcRenderer.send('form-data', params);

  }

  render(){
    return (
      <div className="container">
      <Title/>
      <div className="ui centered cards">
          <div className="ui card" >
          <div hidden={!this.state.isLoading}>
              
                <Dimmer inverted active={this.state.isLoading}>
                  <Loader inverted >Loading</Loader>
                </Dimmer>
              
            </div>
            <div hidden={this.state.isLoading}>
              <Form onSubmitHandler={this.handleSubmit} params={this.state} className={this.state.isLoading ? 'hidden' : ''}/>
            </div>
          </div>

        </div>
      </div>  
    );
  }

}

export default App;
