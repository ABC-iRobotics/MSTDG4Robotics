var fs = require('fs');

class TaskService {
    jsonParser(path){
        var json = fs.readFileSync(path);
        
        var parsedObject = JSON.parse(json);
        return parsedObject;
    }
  }

module.exports = {
    TaskService: TaskService
};