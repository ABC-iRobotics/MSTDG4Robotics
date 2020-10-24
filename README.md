# bin_picking_project

This branch is responsible to generate training images for bin picking problem with OE logos and teach YOLOv3 deep learning algorithm to detect the objects in the bin in real time.
Steps for the neural network training:

[1]: bin_picking_development/PythonClient: Generate trainig images and object details into the database. Images shall be generated in the image_set folder. Training details are stored in a MongoDB database in the background. 

[2]: bin_picking_yolo\yolov3_test: Run getMongodb script in order to generate the the object details in the format required to YOLOv3. These files are generated in the newwwFolderrr folder.

[3]: Create the necessary files to the training
	- Copy the images and their generated text files into bin_picking_yolo\yolov3_upload\datasets_to_oe\obj\obj
	- Copy the train.txt file into bin_picking_yolo\yolov3_upload\datasets_to_oe\obj\
	- Compress obj, obj.data, obj.names and train.txt as obj.zip
	- Upload the zip and yolov3-tiny-obj.cfg files to your Google Drive "Coolab Notebooks/datasets_to_oe
	
[4]: Train your neural network on Google Colab:
https://colab.research.google.com/drive/1i5DjeT6c1CB_ftZAsYP_9uxamb_zP4Uz

[5]:After the training of the yolov3 neural network will have finished, download the generated weights from your Google Drive

[6]:Test your yolo weights with the script: bin_picking_yolo\yolov3_test\Test1\program.py

