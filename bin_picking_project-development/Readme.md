## Deep Learning Framework - Beta 0.0.1

### Installing (Windows)

If you would like to install every component you will need for using the Deep Learning Framework, you can simply run (as Administrator):
 `Install/WIN/install_all.ps1`
This will install Mongodb 3.2.7, Python 3.7 (64bit) and V-REP 3.6.1 (EDU).
You can install these modules separately by running the following scripts:
1. `Install/WIN/mongo_install.ps1`
2. `Install/WIN/python_install.ps1`
3. `Install/WIN/vrep_install.ps1`

### Running (Windows)

You can run the framework with the standard scene with the following script:
`\RunningScript\WIN\generateLearningData.ps1`

IMPORTANT: 

Currently the standard scene had been created to get images to teach a Deep Learning algorythm to solve Bin picking problem. The program will import meshes 10 times from the following path: PythonClient\meshes, and  insert them to the scene above a bin. 

The meshes will have random position, orientation  and color because it will helps to the domain randomization. After this, the program will activate dynamic properties and the meshes will fall down to the bin. When the objects are in the bin, we get the vision sensor's image, and save information about the sceen to the mongoDB.


The purpose of the project is to have generic framework to get sensor datas from selectable scenes and store the properties to the database. To achieve that, I will make the program to accept more arguments, I will create more function to modify the scene, and will make the scene selectable.

### Source code

The source code is under PythonClient folder.

Here is the basic project structure:
	- In the project root there are the `main.py` what is the entry point to the program, this implements the main function and the `Helper.py` class that implements helper functions
	- Necessary code and libraries under `libraries` folder
	- Service classes under `Services` folder
	- Models to store datas to the MongoDb under `DataEntities`
	- Mesh files to import under `meshes` folder
	- V-REP scenes under `vrep_scenes` folder