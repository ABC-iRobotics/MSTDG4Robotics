const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const ipcMain = electron.ipcMain;

const path = require('path');
const url = require('url');
const isDev = require('electron-is-dev');

const util = require('util');
const exec = util.promisify(require('child_process').exec);

const task = require('./Services/TaskService');
const TaskService = task.TaskService;
let mainWindow;

ipcMain.on('get-init-data', (event, arg) => {
  var task = new TaskService();
  var sceneObject = task.jsonParser('./public/Task/tasks.json')
  event.returnValue = sceneObject;
});

ipcMain.on('form-data', (event, arg) => {
    var vrepPath = arg.base.vrepPath;
    var arguments = arg.base.taskName;
    var inputs = arg.inputs;
    for (let i = 0; i < inputs.length; i++) {
      const element = inputs[i];
      arguments += " "+ element.value;
    }
    console.log(arguments);
    exec('python3 ./../../PythonClient/main.py ' + arguments, (error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);
    });

});

function createWindow() {
    mainWindow = new BrowserWindow(
    {
        width: 900, 
        height: 680, 
        webPreferences: 
        {
            nodeIntegration: true
        }
    });
  //mainWindow.webContents.openDevTools()
  mainWindow.loadURL(isDev ? 'http://localhost:3000' : `file://${path.join(__dirname, '../build/index.html')}`);
  mainWindow.on('closed', () => mainWindow = null);
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});