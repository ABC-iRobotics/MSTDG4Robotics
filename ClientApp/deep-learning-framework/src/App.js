import React from 'react';
import './App.css';
import Form from "./Components/Form";
import Title from "./Components/Title";
const {ipcRenderer} = window.require('electron');

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      vrepPath: "",
      meshCount: 0,
      datasetCount: 0,
      title: "Base Details",
      isLoading: false
    };

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  pathConverter(path){
    return path.substring(path.lastIndexOf("\\")+1);
  }
  handleSubmit(params) {
    params.isLoading = true;
    this.setState(params);
    
    params.meshPath = this.pathConverter(params.meshPath)

    ipcRenderer.send('form-data', params);

  }

  render(){
    return (
      <div className="container">
      <Title/>
      <div className="ui centered cards">
        
        <div className="ui card">

            <Form onSubmitHandler={this.handleSubmit} params={this.state} className={this.state.isLoading ? 'hidden' : ''}/>
          
          </div>
        </div>
      </div>  
    );
  }

}

export default App;
