# Import required packages:
import os
import glob
import cv2 as cv
import numpy as np
import time

# PHOTO OR CAMERA
# 0 - PHOTO
# 1 - CAMERA
TYPE = 1


# Sensor constants
# Calibration for simulation environment:

OBJECT_WIDTH_IMPORTVREP = 0.0300000086426735  # vision_sensor_height
OBJECT_DEPTH_IMPORTVREP = 0.118194818496704  # IMAGE_HEIGHT
OBJECT_HEIGHT_IMPORTVREP = 0.160000011324883 # IMAGE_WIDTH

IMAGE_WIDTH = 1.779525755
IMAGE_HEIGHT = 1.779525755

CAMERA_HEIGHT_POSITION = 1.65  # Projection for image level


# #Calibration for real object photos
# OBJECT_WIDTH_IMPORTVREP = 0.040610386#0.04125  # vision_sensor_height
# OBJECT_DEPTH_IMPORTVREP = 0.16#0.16252  # IMAGE_HEIGHT
# OBJECT_HEIGHT_IMPORTVREP = 0.216588727#0.22  # IMAGE_WIDTH
#
# IMAGE_WIDTH = 1.1
# IMAGE_HEIGHT = 1.466666
#
# CAMERA_HEIGHT_POSITION = 1  # measured from bin


OBJECT_WIDTH = OBJECT_HEIGHT_IMPORTVREP
OBJECT_HEIGHT = OBJECT_DEPTH_IMPORTVREP
OBJECT_DEPTH = OBJECT_WIDTH_IMPORTVREP

# Write down conf, nms thresholds,inp width/height
confThreshold = 0.6
nmsThreshold = 0.3
inpWidth = 512
inpHeight = 512
# inpWidth = 1024
# inpHeight = 1024

# Folder of photos
current_dir = os.getcwd() + "\\"
inputfolder = 'test_photos_sim'  # Define by user
# inputfolder = 'test_photos_real'  # Define by user
outfolder = inputfolder + '_out'
inputPathFolder = current_dir + inputfolder
outputPathFolder = current_dir + outfolder
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

# Model configuration
modelConf = 'cfg\\yolov3-tiny-obj.cfg'  # Define by user
modelWeights = 'cfg\\yolov3-tiny-obj.weights'  # Define by user

# Load names of classes and turn that into a list
classesFile = "cfg\\obj.names"
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

def project_object_to_camera_coord(bBoxWidth, bBoxHeight):
    if bBoxHeight > bBoxWidth:
        width = bBoxHeight
    else:
        width = bBoxWidth
    # print("bbHeight:", bBoxHeight, "bbWidth:", bBoxWidth, "width:", width)
    h_obj = OBJECT_WIDTH/width * CAMERA_HEIGHT_POSITION
    # print("hboj_calc:", h_obj)
    h_obj_real_rel = h_obj + OBJECT_DEPTH/2
    # print("h_obj_real:", h_obj_real_rel)
    return h_obj_real_rel

def transform_camera_to_abs_coord(relCenterX, relCenterY, relDepth): # (0,0,0) is the top left place
    absCenterX = relCenterX + IMAGE_WIDTH/2
    absCenterY = relCenterY + IMAGE_HEIGHT/2
    absDepth = CAMERA_HEIGHT_POSITION - relDepth

    return absCenterX, absCenterY, absDepth


def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIDs = []
    confidences = []
    boxes = []
    relCenterX_array = []
    relCenterY_array = []
    relDepth_array = []
    absCenterX_array = []
    absCenterY_array = []
    absDepth_array = []
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

                # print original position and size
                # print("Class:", classID)
                # print("Position:", detection[0], detection[1])
                # print("BBSize:", detection[2], detection[3])

                relCenterX_original = detection[0]
                relCenterY_original = detection[1]
                relWidth_original = detection[2]
                relHeight_original = detection[3]
                relCenterX = (relCenterX_original - 0.5) * IMAGE_WIDTH / 2
                relCenterY = (relCenterY_original - 0.5) * IMAGE_HEIGHT / 2
                # print("Relative position\nx:{0}\ty:{1}".format(relCenterX,relCenterY))
                # print("relwidth: {}, relheight: {}".format(relWidth_original, relHeight_original))
                # print("relwidthFrame: {}, relheightFrame: {}".format(relWidth_original*IMAGE_WIDTH , relHeight_original*IMAGE_HEIGHT ))

                # relDepth = project_object_to_camera_coord(relWidth_original, relHeight_original)
                relDepth = project_object_to_camera_coord(relWidth_original*IMAGE_WIDTH, relHeight_original*IMAGE_HEIGHT)
                absCenterX, absCenterY, absDepth = transform_camera_to_abs_coord(relCenterX, relCenterY, relDepth)
                # print("calc_width::", relWidth_original)
                # print("Prognosed depth:", relDepth)
                relCenterX_array.append(relCenterX)
                relCenterY_array.append(relCenterY)
                relDepth_array.append(relDepth)
                absCenterX_array.append(absCenterX)
                absCenterY_array.append(absCenterY)
                absDepth_array.append(absDepth)

                left = int(centerX - width / 2)
                top = int(centerY - height / 2)

                classIDs.append(classID)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    relPos_array = []
    absPos_array = []
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        relPos_array = [relCenterX_array[i], relCenterY_array[i], relDepth_array[i]]
        absPos_array = [absCenterX_array[i], absCenterY_array[i], absDepth_array[i]]
        print('\n')
        print("Relative position\nx:{}\ty:{}, \tz:{}".format(relPos_array[0], relPos_array[1], relPos_array[2]))
        print("Absolute position\nx:{}\ty:{}, \tz:{}".format(absPos_array[0], absPos_array[1], absPos_array[2]))
        #print("Prognosed depth:", relDepth_array[i])
        drawPred(frame, classIDs[i], confidences[i], left, top, left + width, top + height)


def drawPred(frame, classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 5)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # A fancier display of the label from learnopencv.com
    # Display the label at the top of the bounding box
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    # cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 5)


def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()

    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def loadImages(path="."):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


def object_detection_from_image(inputPathFolder, outputPathFolder, net):
    fileNames = loadImages(outputPathFolder)

    data_path = os.path.join(inputPathFolder, '*.jpg')
    files = glob.glob(data_path)
    frames = []
    for f1 in files:
        img = cv.imread(f1)
        frames.append(img)

    num = 0

    for frame in frames:
        # outName = str(num) + ".jpg"
        outName = "{:04}".format(num) + ".jpg"
        # print("Outname: ", outName)
        num += 1
        blobImage = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
        # Set the input the net
        net.setInput(blobImage)
        start = time.time()
        outsImage = net.forward(getOutputsNames(net))
        end = time.time()

        # Showing spent time for forward pass
        print('\nObjects Detection took {:.5f} seconds'.format(end - start))
        postprocess(frame, outsImage)
        # cv.imshow('showiamgee', image)
        cv.imwrite(os.path.join(outputPathFolder, outName), frame)

        cv.waitKey(0)
        cv.destroyAllWindows()

def object_detection_from_camera(net):
    # # Process inputs
    # winName = 'DL OD with OpenCV'
    # cv.namedWindow(winName, cv.WINDOW_NORMAL)
    # cv.resizeWindow(winName, 1000, 1000)
    # cap = cv.VideoCapture(0)

    # Defining 'VideoCapture' object
    # and reading stream video from camera
    camera = cv.VideoCapture(0)

    # Preparing variables for spatial dimensions of the frames
    h, w = None, None
    while True:
        # Capturing frame-by-frame from camera
        _, frame = camera.read()

        # Getting spatial dimensions of the frame
        # we do it only once from the very beginning
        # all other frames have the same dimension
        if w is None or h is None:
            # Slicing from tuple only first two elements
            h, w = frame.shape[:2]

        """
        Start of:
        Getting blob from current frame
        """

        # Getting blob from current frame
        # The 'cv2.dnn.blobFromImage' function returns 4-dimensional blob from current
        # frame after mean subtraction, normalizing, and RB channels swapping
        # Resulted shape has number of frames, number of channels, width and height
        # E.G.:
        # blob = cv.dnn.blobFromImage(image, scalefactor=1.0, size, mean, swapRB=True)
        blob = cv.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                    swapRB=True, crop=False)

        """
        End of:
        Getting blob from current frame
        """

        """
        Start of:
        Implementing Forward pass
        """

        # Implementing forward pass with our blob and only through output layers
        # Calculating at the same time, needed time for forward pass
        net.setInput(blob)  # setting blob as input to the network
        start = time.time()
        output_from_network = net.forward(getOutputsNames(net))
        end = time.time()

        # Showing spent time for single current frame
        # print('Current frame took {:.5f} seconds'.format(end - start))

        """
        End of:
        Implementing Forward pass
        """
        postprocess(frame, output_from_network)

        """
        Start of:
        Showing processed frames in OpenCV Window
        """

        # Showing results obtained from camera in Real Time

        # Showing current frame with detected objects
        # Giving name to the window with current frame
        # And specifying that window is resizable
        cv.namedWindow('YOLO v3 Real Time Detections', cv.WINDOW_NORMAL)
        # Pay attention! 'cv2.imshow' takes images in BGR format
        cv.imshow('YOLO v3 Real Time Detections', frame)

        # Breaking the loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        """
        End of:
        Showing processed frames in OpenCV Window
        """


# Set up the net

net = cv.dnn.readNetFromDarknet(modelConf, modelWeights)  # Reads a network model stored in Darknet model files
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)  # Enum of computation backends supported by layers.
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)  # Enum of target devices for computations.

if TYPE == 0:  # PHOTOS
    object_detection_from_image(inputPathFolder, outputPathFolder, net)
else:  # CAMERA
    object_detection_from_camera(net)
