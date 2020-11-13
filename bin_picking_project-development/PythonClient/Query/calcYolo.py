import numpy as np
import math
import Query.quaternions as quat


def rotBoundBox(q, object, size, absHeight, absWidth, binPosHeight, binHeight):
    x_height = size[0]
    y_depth = size[1]
    z_width = size[2]
    #maxDiagonal= math.sqrt((math.pow(x_height,2))+(math.pow(y_depth,2))+(math.pow(z_width,2)))
    #maxDiagonalOnYolo = maxDiagonal*1.82115/1.458/2.1028367
    maxDiagonalOnYolo = MaxDiagonalYolo(x_height, y_depth, z_width, absHeight, absWidth, binPosHeight, binHeight)
    boundBox1=np.array([-x_height/2, -y_depth/2, -z_width/2])
    boundBox2=np.array([-x_height/2, -y_depth/2, z_width/2])
    boundBox3=np.array([-x_height/2, y_depth/2, -z_width/2])
    boundBox4=np.array([-x_height/2, y_depth/2, z_width/2])
    boundBox5=np.array([x_height/2, -y_depth/2, -z_width/2])
    boundBox6=np.array([x_height/2, -y_depth/2, z_width/2])
    boundBox7=np.array([x_height/2, y_depth/2, -z_width/2])
    boundBox8=np.array([x_height/2, y_depth/2, z_width/2])
    #Create quaternion vector from database
     #modified by DGU 20200921 V-rep gives x,y,z,w -> rotate_vector uses w,x,y,z
    quat1 = np.array([q[3], q[0], q[1], q[2]])
    boundBox1Transf=quat.rotate_point(boundBox1,quat1)
    boundBox2Transf=quat.rotate_point(boundBox2,quat1)
    boundBox3Transf=quat.rotate_point(boundBox3,quat1)
    boundBox4Transf=quat.rotate_point(boundBox4,quat1)
    boundBox5Transf=quat.rotate_point(boundBox5,quat1)
    boundBox6Transf=quat.rotate_point(boundBox6,quat1)
    boundBox7Transf=quat.rotate_point(boundBox7,quat1)
    boundBox8Transf=quat.rotate_point(boundBox8,quat1)
    xCoordList=[boundBox1Transf[0],boundBox2Transf[0], boundBox3Transf[0],boundBox4Transf[0],boundBox5Transf[0],boundBox6Transf[0],boundBox7Transf[0],boundBox8Transf[0]]
    yCoordList=[boundBox1Transf[1],boundBox2Transf[1], boundBox3Transf[1],boundBox4Transf[1],boundBox5Transf[1],boundBox6Transf[1],boundBox7Transf[1],boundBox8Transf[1]]
    zCoordList=[boundBox1Transf[2],boundBox2Transf[2], boundBox3Transf[2],boundBox4Transf[2],boundBox5Transf[2],boundBox6Transf[2],boundBox7Transf[2],boundBox8Transf[2]]

    for i in range(len(xCoordList)):
        #print("xCoordList[i]:", xCoordList[i])
        #xCoordList[i] = (object_x-xCoordList[i])*1.821115/2.1028367/(object_z-zCoordList[i])
        xCoordList[i] = (object[0] - xCoordList[i]) * absHeight / absWidth / (object[2] - zCoordList[i])
    for i in range(len(yCoordList)):
        yCoordList[i] = (object[1]-yCoordList[i])*absHeight/absWidth/(object[2]-zCoordList[i])#xCoordList[i]
    for i in range(len(zCoordList)):
        zCoordList[i] = (object[2]-zCoordList[i])*absHeight/absWidth/(object[2]-zCoordList[i])#xCoordList[i]
    z=maxDiff(zCoordList)
    boundBoxWidth=minFunc(maxDiagonalOnYolo,maxDiff(xCoordList))#(maxDiff(zCoordList))#*1.821115/2.1/(height_VisionSensor-max(zCoordList))#*1.8/2.1/z
    boundBoxHeight=minFunc(maxDiagonalOnYolo,maxDiff(yCoordList))#*1.821115/2.1/(height_VisionSensor-max(zCoordList))#*1.8/2.1/z

    return boundBoxHeight, boundBoxWidth


def MaxDiagonalYolo(size_x, size_y, size_z, absHeight, absWidth, binPosHeight = 0, binHeight = 0):
    x_height = size_x
    y_depth = size_y
    z_width = size_z
    binHeightThreshold = binPosHeight + 0.075 * binHeight
    maxDiagonal= math.sqrt((math.pow(x_height,2))+(math.pow(y_depth,2))+(math.pow(z_width,2)))
    limMax = maxDiagonal*absHeight/(absHeight-binHeightThreshold)/absWidth
    return limMax


def GetObjectTopSurface(absOrientation):
    vec1 = [1, 1, 1]
    vec2 = [0, 1, 1]
    quat_obj = np.array([absOrientation[3], absOrientation[0], absOrientation[1], absOrientation[2]])
    transformedVec1 = quat.rotate_vector(vec1, quat_obj)
    transformedVec2 = quat.rotate_vector(vec2, quat_obj)
    if transformedVec1[2] > transformedVec2[2]:
        topSurface = 0  # 0: 3O, 1:OE
    else:
        topSurface = 1
    return topSurface

def IsInBin(absPos_z, binPosHeight, binHeight):
    binHeightThreshold = binPosHeight + 0.075 * binHeight
    isInBin = absPos_z > binHeightThreshold #Height of bin is around 0.45
    return isInBin

def IsOnImage(x,y):
    if x > 0 and x < 1 and y > 0 and y < 1:
        isOnImage = 1
    else:
        isOnImage = 0
    return isOnImage

def minFunc(a,b):
    if a<b:
        return a
    else:
        return b


def maxDiff(a):
    vmin = a[0]
    vmax = a[0]
    dmax = 0
    for i in range(len(a)):
        if (a[i] < vmin):
            vmin = a[i]
        if (a[i] > vmax):
            vmax = a[i]
    dmax=vmax-vmin
    return dmax


