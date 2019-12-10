# Import required packages:
import os
# noinspection PyUnresolvedReferences
#import tkinter
from tkinter import *
from tkinter import filedialog
import glob
import cv2 as cv
import numpy as np

# Write down conf, nms thresholds,inp width/height
confThreshold = 0.7
nmsThreshold = 0.7
inpWidth = 416
inpHeight = 416

# Load names of classes and turn that into a list
classesFile = "obj.names"
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Model configuration
modelConf = 'yolov3-tiny-obj.cfg'
modelWeights = 'yolov3-tiny-obj_final.weights'


def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIDs = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:

            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > confThreshold:
                centerX = int(detection[0] * frameWidth)
                centerY = int(detection[1] * frameHeight)

                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)

                left = int(centerX - width / 2)
                top = int(centerY - height / 2)

                classIDs.append(classID)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]

        drawPred(classIDs[i], confidences[i], left, top, left + width, top + height)


def drawPred(classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 3)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # A fancier display of the label from learnopencv.com
    # Display the label at the top of the bounding box
    # labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    # top = max(top, labelSize[1])
    # cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
    # (255, 255, 255), cv.FILLED)
    # cv.re ctangle(frame, (left,top),(right,bottom), (255,255,255), 1 )
    # cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)


def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()

    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]





def loadImages(path="."):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


# browse folder
root = Tk()
root.withdraw() #use to hide tkinter window

def search_for_file_path (Text):
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title=Text)
    """if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
        """
#print the chosen path
    return tempdir


inputPathFolder = search_for_file_path("Please select your input folder")
outputPathFolder = search_for_file_path("Please select your output folder")
#print ("\nfile_path_variable = ", inputPathFolder,"\n", outputPathFolder)

# Set up the net

net = cv.dnn.readNetFromDarknet(modelConf, modelWeights)  # Reads a network model stored in Darknet model files
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)  # Enum of computation backends supported by layers.
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)  # Enum of target devices for computations.

# Process inputs
winName = 'DL OD with OpenCV'
# cv.namedWindow(winName, cv.WINDOW_NORMAL)
# cv.resizeWindow(winName, 1000, 1000)
#
# cap = cv.VideoCapture(0)
fileNames = loadImages(outputPathFolder)

data_path = os.path.join(inputPathFolder,'*.jpg')
#print("Datapath: ", data_path)
files = glob.glob(data_path)
#print("files: ", files)
frames = []
for f1 in files:
    img = cv.imread(f1)
    frames.append(img)
#print("Frames: ", frames)
"""for file in fileNames:
    images.append(cv.imread(file, cv.IMREAD_UNCHANGED))
"""
#frame = cv.imread(inputPathFolder)
for frame in frames:
    blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
# Set the input the the net
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))

    postprocess(frame, outs)

# show the image

#cv.imshow('image', frame)
# fileName = os.listdir(imagePath)
#print("filenames: ", fileNames)
num = 0
# outPath =input("Give me the path of output folder: ")
# print(outPath)
#outPath = r'C:\Users\david9613\Desktop\OE\yolov3_train\Test1\OutTeams'
for frame in frames:
    #outName = str(num) + ".jpg"
    outName = "{:04}".format(num)+".jpg"
    #print("Outname: ", outName)
    num += 1
    blobImage = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
    # Set the input the net
    net.setInput(blobImage)
    outsImage = net.forward(getOutputsNames(net))
    postprocess(frame, outsImage)
    # cv.imshow('showiamgee', image)
    cv.imwrite(os.path.join(outputPathFolder, outName), frame)

cv.waitKey(0)
cv.destroyAllWindows()
