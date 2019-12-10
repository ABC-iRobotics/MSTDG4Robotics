# bin_picking_project

This branch is responsible to process the images about the bin and the items within. YOLOv3 algorithm is used to imageprocessing that is a neural network based deep-learning algorithm. The neural network should taught with the images of items. These training images come from previous part of the project or you can download some simple images from Google, for instance with the browser extension "Fatkun Batch Download Image".
Steps for the neural network training:
[1]: label the images with YoloLabel app
        -define the object names within class_list.txt
        -copy images to obj folder
[2]: Make Train.txt by the python script:
        - copy obj folder with the images
        - run the script and train.txt will be generated
[3]: Create the configuration files can be found in yolov3_upload folder:
        - copy there the labeled obj folder (jpg,txt)
        - copy there the generated train.txt
        - create obj.data, obj.names and yolov3-tiny-obj.cfg files based on Darknet instructions: https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects
        - create obj.zip file from obj folder, train.txt, obj.data, obj.names
        - upload obj.zip and yolov3-tiny-obj.cfg files to Google Drive e.g.: My Drive/Coolab Notebooks/datasets_to_buses
[4]: Train neural network:
https://colab.research.google.com/drive/1i5DjeT6c1CB_ftZAsYP_9uxamb_zP4Uz
      - Run the following scripts on Google Colab, first you have to mount your google drive. Check whether your files are uploaded to the aforementioned folder. If the path is different, you should overwrite 2 commands in the script
      -If the training finishes, you are able to download the generated weights from Google Drrive
[5]: Process some input images with the trained neural network:
      - Copy obj.names, the weights, configuration file and images folder to yolov3_test/Test1 folder
      - Run program.py script and select the input and output folders by GUI
