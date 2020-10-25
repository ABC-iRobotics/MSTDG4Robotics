from pymongo import MongoClient
import psycopg2
import pymongo
import pprint
import os.path
import numpy as np
import math
_MAX_FLOAT = np.maximum_sctype(np.float)
_FLOAT_EPS = np.finfo(np.float).eps


def main():
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["DeepLearningTrainingSet"]
    mycol = mydb["BinPicking"]
    results = mycol.find()
    # rest_tup = create_restaurants(results)
    # rest_records = rest_tup[0]
    # rest_headers = rest_tup[1]
    # create_table(rest_records, rest_headers, './restaurants.csv')
    results = mycol.find()
    #Query the properties of each object from the database of training data
    objects_tup = create_objects(results)
    #print(objects_tup)
    objects_records = objects_tup[0]
    #print(objects_records[0][0])
    objects_headers = objects_tup[1]
    #print(objects_headers)
    #create_table(objects_records, objects_headers, './objects.csv')
    #Transform the object into YOLO and print in text files
    create_text(objects_records, objects_headers, 'image_set\\','.jpg')

def create_objects(results):
    '''
    Take the query outcome and convert to a list and return it.
    It also defines headers and return it.
    '''
    records = []
    headers = ['id','imageUrl','absolutePosition1', 'absolutePosition2', 'absolutePosition3', 'absoluteOrientation1','absoluteOrientation2','absoluteOrientation3','absoluteOrientation4','relativePosition1', 'relativePosition2', 'relativePosition3', 'relativeOrientation1','relativeOrientation2','relativeOrientation3','relativeOrientation4']
    for record in results:
        for position in record['fixtures']:
            tmp = []
            try:
                tmp.append(str(record['_id']).split("(")[0])
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(record['imageUrl'])
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['absolutePosition'][0]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['absolutePosition'][1]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['absolutePosition'][2]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['absoluteOrientation'][0]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['absoluteOrientation'][1]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['absoluteOrientation'][2]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['absoluteOrientation'][3]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['relativePosition'][0]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['relativePosition'][1]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['relativePosition'][2]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['relativeOrientation'][0]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['relativeOrientation'][1]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['relativeOrientation'][2]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['relativeOrientation'][3]))
            except IndexError:
                tmp.append('NA')
            records.append(tmp)
    return records, headers

def create_table(records, headers, file_path):
    "Take a list of records and headers and generate csv"
    f = open(file_path, 'w', encoding='utf-8')
    row_len = len(headers)
    f.write(format_list(headers, row_len, ';', '"'))
    for record in records:
        f.write(format_list(record, row_len, ';', '"'))
    f.close()
    print('CSV file successfully created: {}'.format(file_path))

def create_text(records, headers, beg, end):
    "DGU: Rotate the bounding boxes and print in the textes"
    tmp=[]
    temp=""
    i = 0
    tmp2=''
    file_name='NA'
    trainFile_name = 'train.txt'
    imageNames = ""
    save_path = os.getcwd() + "\\newwwFolderrr"
    for record in records:
        #print("x:", float(record[2]), "\ty:", float(record[3]), "\tz:", float(record[4])
        #print("x_rel:\t", float(record[9]), "\ty_rel:\t", float(record[10]), "\tz_rel:\t", float(record[11]),"\nrel_quaternions:",float(record[12]), ", ",float(record[13]), ", ", float(record[14]), ", ", float(record[15]))
        #print("x:",float(record[2]),"\ty:",float(record[3]),"\tz:",float(record[4]),"\nquaternions:",float(record[5]), ", ",float(record[6]), ", ", float(record[7]), ", ", float(record[8]))
        midX=(((float(record[9]) - 0)*1.821115)/((float(record[11]))*(-2.1028367))) + 0.5
        midY=(((float(record[10]) - 0) * 1.821115) / (float(record[11]) * (2.1028367))) + 0.5
        boundingBoxSize = rotBoundBox(float(record[12]), float(record[13]), float(record[14]), float(record[15]), float(record[9]), float(record[10]), float(record[11]))
        #boundingBoxSize = [0.1, 0.1]

    #Determine whether the object orientation is OE or EO
        vec_to_OEorientation_1 = [1, 1, 1]
        vec_to_OEorientation_2 = [0, 1, 1]
        quat_obj = np.array([float(record[15]), float(record[12]), float(record[13]), float(record[14])])
        transformed_vector_to_OEorientation_1 = rotate_vector_original(vec_to_OEorientation_1, quat_obj)
        transformed_vector_to_OEorientation_2 = rotate_vector_original(vec_to_OEorientation_2, quat_obj)
        if transformed_vector_to_OEorientation_1[2] > transformed_vector_to_OEorientation_2[2]:
            isOE_orientation = 1 #0: EO, 1:OE
        else:
            isOE_orientation = 0
        isInBin = float(record[11]) < 1.5

    #Write the object YOLO details into each text file
        if record[1]==tmp2:
            if isInBin:
                temp=temp + str(isOE_orientation) + " " + str(midX) +" " + str(midY) + " " + str(boundingBoxSize[0]) + " " + str(boundingBoxSize[1]) + str('\n')
        elif file_name != 'NA':
            temp=temp.replace("[","").replace("]","").replace("'","").replace(",","")
            completeName = os.path.join(save_path, file_name)
            f = open(completeName, 'w', encoding='utf-8')
            f.write(str(temp))
            f.close()
            imageNames = imageNames + "data/obj/" + find_between(record[1], beg, end) + ".jpg\n"
            if isInBin:
                temp = str(isOE_orientation) + " " + str(midX) + " " + str(midY) + " " + str(boundingBoxSize[0]) + " " + str(
                    boundingBoxSize[1]) + str('\n')
            else:
                temp = ""
        else:
            if isInBin:
                temp = str(isOE_orientation) + " "+ str(midX) + " " + str(midY) + " " + str(boundingBoxSize[0]) + " " + str(
                    boundingBoxSize[1]) + str('\n')
            else:
                temp = ""
            imageNames = imageNames + "data/obj/" +  find_between(record[1], beg, end) + ".jpg\n"

        tmp2=record[1]
        file_name = find_between(record[1], beg, end) + ".txt"
    temp=temp.replace("[","").replace("]","").replace("'","").replace(",","")
    completeName = os.path.join(save_path, file_name)
    f = open(completeName, 'w', encoding='utf-8')
    f.write(str(temp))
    f.close()

    #Create train.txt:
    completeImageName = os.path.join(save_path, trainFile_name)
    f = open(completeImageName, 'w', encoding='utf-8')
    f.write(str(imageNames))
    f.close()




def format_list(list, length, delimiter, quote):
    counter = 1
    string = ''
    for record in list:
        if counter == length:
            string += quote + record + quote + '\n'
        else:
            string += quote + record + quote + delimiter
        counter += 1
    return string

def pg_load_table(file_path, table_name):
    try:
        conn = psycopg2.connect("dbname='mydatahack' user='mydatahack' host='localhost' password='Password1'")
        print("Connecting to Database")
        cur = conn.cursor()
        f = open(file_path, "r", encoding='utf-8')
        cur.execute("Truncate {} Cascade;".format(table_name))
        print("Truncated {}".format(table_name))
        cur.copy_expert("copy {} from STDIN CSV HEADER".format(table_name), f)
        cur.execute("commit;")
        print("Loaded data into {}".format(table_name))
        conn.close()
        print("DB connection closed.")
    except Exception as e:
        print("Error: {}".format(str(e)))

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
def quat2mat(q):
    ''' Calculate rotation matrix corresponding to quaternion

    Parameters
    ----------
    q : 4 element array-like

    Returns
    -------
    M : (3,3) array
      Rotation matrix corresponding to input quaternion *q*

    Notes
    -----
    Rotation matrix applies to column vectors, and is applied to the
    left of coordinate vectors.  The algorithm here allows quaternions that
    have not been normalized.

    References
    ----------
    Algorithm from http://en.wikipedia.org/wiki/Rotation_matrix#Quaternion

    Examples
    --------
    >>> import numpy as np
    >>> M = quat2mat([1, 0, 0, 0]) # Identity quaternion
    >>> np.allclose(M, np.eye(3))
    True
    >>> M = quat2mat([0, 1, 0, 0]) # 180 degree rotn around axis 0
    >>> np.allclose(M, np.diag([1, -1, -1]))
    True
    '''
    w, x, y, z = q
    Nq = w*w + x*x + y*y + z*z
    if Nq < _FLOAT_EPS:
        return np.eye(3)
    s = 2.0/Nq
    X = x*s
    Y = y*s
    Z = z*s
    wX = w*X; wY = w*Y; wZ = w*Z
    xX = x*X; xY = x*Y; xZ = x*Z
    yY = y*Y; yZ = y*Z; zZ = z*Z
    return np.array(
           [[ 1.0-(yY+zZ), xY-wZ, xZ+wY ],
            [ xY+wZ, 1.0-(xX+zZ), yZ-wX ],
            [ xZ-wY, yZ+wX, 1.0-(xX+yY) ]])
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

def maxLimit(width):
    x_height = 0.024
    y_depth = 0.09456
    z_width = 0.128
    maxDiagonal= math.sqrt((math.pow(x_height,2))+(math.pow(y_depth,2))+(math.pow(z_width,2)))
    limMax = maxDiagonal*1.82115/1.458/2.1028367
    if limMax < width:
        return width
    else:
        return limMax

def minFunc(a,b):
    if a<b:
        return a
    else:
        return b

def rotate_vector_original(v, q):
    ''' Apply transformation in quaternion `q` to vector `v`

    Parameters
    ----------
    v : 3 element sequence
       3 dimensional vector
    q : 4 element sequence
       w, i, j, k of quaternion

    Returns
    -------
    vdash : array shape (3,)
       `v` rotated by quaternion `q`

    Notes
    -----
    See: http://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Describing_rotations_with_quaternions
    '''
    varr = np.zeros((4,))
    varr[1:] = v
    return qmult(q, qmult(varr, qconjugate(q)))[1:]


def rotate_vector(v, q):
    ''' Apply transformation in quaternion `q` to vector `v`

    Parameters
    ----------
    v : 3 element sequence
       3 dimensional vector
    q : 4 element sequence
       w, i, j, k of quaternion

    Returns
    -------
    vdash : array shape (3,)
       `v` rotated by quaternion `q`

    Notes
    -----
    See: http://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Describing_rotations_with_quaternions
    '''
    #varr = np.zeros((4,))
    varr = np.ones((4,))
    varr[0:3]= v #DGU: commented out on testing purpose - 20200921
    #varr[1:] = v #DGU: pasted on testing purpose - 20200921
    #print("v=",v,"\nvarr:",varr)
    #print(qmult(q, qmult(varr, qconjugate(q))))
    return qmult(q, qmult(varr, qconjugate(q)))[1:]
def qmult(q1, q2):
    ''' Multiply two quaternions

    Parameters
    ----------
    q1 : 4 element sequence
    q2 : 4 element sequence

    Returns
    -------
    q12 : shape (4,) array

    Notes
    -----
    See : http://en.wikipedia.org/wiki/Quaternions#Hamilton_product
    '''
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 + y1*w2 + z1*x2 - x1*z2
    z = w1*z2 + z1*w2 + x1*y2 - y1*x2
    return np.array([w, x, y, z])
def qmult_bkp(q1, q2):
    ''' Multiply two quaternions

    Parameters
    ----------
    q1 : 4 element sequence
    q2 : 4 element sequence

    Returns
    -------
    q12 : shape (4,) array

    Notes
    -----
    See : http://en.wikipedia.org/wiki/Quaternions#Hamilton_product
    '''
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 + y1*w2 + z1*x2 - x1*z2
    z = w1*z2 + z1*w2 + x1*y2 - y1*x2
    return np.array([w, x, y, z])
def qconjugate(q):
    ''' Conjugate of quaternion

    Parameters
    ----------
    q : 4 element sequence
       w, i, j, k of quaternion

    Returns
    -------
    conjq : array shape (4,)
       w, i, j, k of conjugate of `q`
    '''
    return np.array(q) * np.array([1.0, -1, -1, -1])
def rotBoundBox(q1, q2, q3, q4, object_x, object_y, object_z):
    #Give the size of the object! (X,Y,Z)
    x_height = 0.024
    y_depth = 0.09456
    z_width = 0.128
    maxDiagonal= math.sqrt((math.pow(x_height,2))+(math.pow(y_depth,2))+(math.pow(z_width,2)))
    maxDiagonalOnYolo = maxDiagonal*1.82115/1.458/2.1028367
    vector_object = [x_height, y_depth, z_width]#DGU - 20200926
    boundBox1=np.array([-x_height/2, -y_depth/2, -z_width/2])
    boundBox2=np.array([-x_height/2, -y_depth/2, z_width/2])
    boundBox3=np.array([-x_height/2, y_depth/2, -z_width/2])
    boundBox4=np.array([-x_height/2, y_depth/2, z_width/2])
    boundBox5=np.array([x_height/2, -y_depth/2, -z_width/2])
    boundBox6=np.array([x_height/2, -y_depth/2, z_width/2])
    boundBox7=np.array([x_height/2, y_depth/2, -z_width/2])
    boundBox8=np.array([x_height/2, y_depth/2, z_width/2])
    #Create quaternion vector from database
    #quat1_original=np.array([q1, q2, q3, q4])
    quat1_original = np.array([q4, q1, q2, q3]) #modified by DGU 20200921 V-rep gives x,y,z,w -> rotate_vector uses w,x,y,z
    rotMx =np.array([0,0,1,0,0,-1,0,0,1,0,0,0,0,0,0,1]).reshape(4,4)
    quat1=rotMx.dot(quat1_original)
    quat1=quat1_original
    boundBox1Transf=rotate_vector(boundBox1,quat1)
    boundBox2Transf=rotate_vector(boundBox2,quat1)
    boundBox3Transf=rotate_vector(boundBox3,quat1)
    boundBox4Transf=rotate_vector(boundBox4,quat1)
    boundBox5Transf=rotate_vector(boundBox5,quat1)
    boundBox6Transf=rotate_vector(boundBox6,quat1)
    boundBox7Transf=rotate_vector(boundBox7,quat1)
    boundBox8Transf=rotate_vector(boundBox8,quat1)
#    boundBox1Transf=rotate_vector_original(boundBox1,quat1) #DGU - 20200926
#    boundBox2Transf=rotate_vector_original(boundBox2,quat1) #DGU - 20200926
#    boundBox3Transf=rotate_vector_original(boundBox3,quat1) #DGU - 20200926
#    boundBox4Transf=rotate_vector_original(boundBox4,quat1) #DGU - 20200926
#    boundBox5Transf=rotate_vector_original(boundBox5,quat1) #DGU - 20200926
#    boundBox6Transf=rotate_vector_original(boundBox6,quat1) #DGU - 20200926
#    boundBox7Transf=rotate_vector_original(boundBox7,quat1) #DGU - 20200926
#    boundBox8Transf=rotate_vector_original(boundBox8,quat1) #DGU - 20200926
    #print(boundBox8Transf)
    #print(height_VisionSensor)
    rotated_vector_object = rotate_vector_original(vector_object, quat1_original) #DGU - 20200926
    xCoordList=[boundBox1Transf[0],boundBox2Transf[0], boundBox3Transf[0],boundBox4Transf[0],boundBox5Transf[0],boundBox6Transf[0],boundBox7Transf[0],boundBox8Transf[0]]
    yCoordList=[boundBox1Transf[1],boundBox2Transf[1], boundBox3Transf[1],boundBox4Transf[1],boundBox5Transf[1],boundBox6Transf[1],boundBox7Transf[1],boundBox8Transf[1]]
    zCoordList=[boundBox1Transf[2],boundBox2Transf[2], boundBox3Transf[2],boundBox4Transf[2],boundBox5Transf[2],boundBox6Transf[2],boundBox7Transf[2],boundBox8Transf[2]]

    for i in range(len(xCoordList)):
        #print("xCoordList[i]:", xCoordList[i])
        xCoordList[i] = (object_x-xCoordList[i])*1.821115/2.1028367/(object_z-zCoordList[i])
    for i in range(len(yCoordList)):
        yCoordList[i] = (object_y-yCoordList[i])*1.821115/2.1028367/(object_z-zCoordList[i])#xCoordList[i]
    for i in range(len(zCoordList)):
        zCoordList[i] = (object_z-zCoordList[i])*1.821115/2.1028367/(object_z-zCoordList[i])#xCoordList[i]
    z=maxDiff(zCoordList)#*1.8/2.1/z
    boundBoxWidth=minFunc(maxDiagonalOnYolo,maxDiff(xCoordList))#(maxDiff(zCoordList))#*1.821115/2.1/(height_VisionSensor-max(zCoordList))#*1.8/2.1/z
    boundBoxHeight=minFunc(maxDiagonalOnYolo,maxDiff(yCoordList))#*1.821115/2.1/(height_VisionSensor-max(zCoordList))#*1.8/2.1/z

#    for i in range(len(zCoordList)):
#        #print("xCoordList[i]:", xCoordList[i])
#        zCoordList[i] = height_VisionSensor - float(zCoordList[i])
#    for i in range(len(yCoordList)):
#        yCoordList[i] = yCoordList[i]*1.821115/2.1/1.5#height_VisionSensor#xCoordList[i]
#    for i in range(len(xCoordList)):
#        xCoordList[i] = xCoordList[i]*1.821115/2.1/1.5#height_VisionSensor#xCoordList[i]
#    z=maxDiff(xCoordList)#*1.8/2.1/z
#    boundBoxWidth=(maxDiff(xCoordList))#*1.8/2.1/z
#    boundBoxHeight=(maxDiff(yCoordList))#*1.8/2.1/z

    #zBoundBox = height_VisionSensor - rotated_vector_object[0] #DGU - 20200926
    #boundBoxWidth = rotated_vector_object[2]*1.821115/2.1/zBoundBox #DGU - 20200926
    #boundBoxHeight = rotated_vector_object[1]*1.821115/2.1/zBoundBox #DGU - 20200926
    return boundBoxHeight, boundBoxWidth
    #print("x:",x, "\nwidth:", boundBoxWidth,"\nHeight:",boundBoxHeight)
def rotBoundBox_bkp(q1, q2, q3, q4, z):
    boundBox1=np.array([-0.064, -0.04728, -0.012])
    boundBox2=np.array([-0.064, -0.04728, 0.012])
    boundBox3=np.array([-0.064, 0.04728, -0.012])
    boundBox4=np.array([-0.064, 0.04728, 0.012])
    boundBox5=np.array([0.064, -0.04728, -0.012])
    boundBox6=np.array([0.064, -0.04728, 0.012])
    boundBox7=np.array([0.064, 0.04728, -0.012])
    boundBox8=np.array([0.064, 0.04728, 0.012])
    quat1_original=np.array([q1, q2, q3, q4])
    rotMx =np.array([0,0,1,0,0,-1,0,0,-1,0,0,0,0,0,0,1]).reshape(4,4)
    quat1=rotMx.dot(quat1_original)
    #quat1=quat1_original
    boundBox1Transf=rotate_vector(boundBox1,quat1)
    boundBox2Transf=rotate_vector(boundBox2,quat1)
    boundBox3Transf=rotate_vector(boundBox3,quat1)
    boundBox4Transf=rotate_vector(boundBox4,quat1)
    boundBox5Transf=rotate_vector(boundBox5,quat1)
    boundBox6Transf=rotate_vector(boundBox6,quat1)
    boundBox7Transf=rotate_vector(boundBox7,quat1)
    boundBox8Transf=rotate_vector(boundBox8,quat1)
    xCoordList=[boundBox1Transf[0],boundBox2Transf[0], boundBox3Transf[0],boundBox4Transf[0],boundBox5Transf[0],boundBox6Transf[0],boundBox7Transf[0],boundBox8Transf[0]]
    for i in range(len(xCoordList)):
        xCoordList[i] = z - float(xCoordList[i])
    yCoordList=[boundBox1Transf[1],boundBox2Transf[1], boundBox3Transf[1],boundBox4Transf[1],boundBox5Transf[1],boundBox6Transf[1],boundBox7Transf[1],boundBox8Transf[1]]
    zCoordList=[boundBox1Transf[2],boundBox2Transf[2], boundBox3Transf[2],boundBox4Transf[2],boundBox5Transf[2],boundBox6Transf[2],boundBox7Transf[2],boundBox8Transf[2]]
    for i in range(len(yCoordList)):
        yCoordList[i] = yCoordList[i]*1.821115/2.1/xCoordList[i]
    for i in range(len(zCoordList)):
        zCoordList[i] = zCoordList[i]*1.821115/2.1/xCoordList[i]
    x=maxDiff(xCoordList)#*1.8/2.1/z
    boundBoxWidth=(maxDiff(zCoordList))#*1.8/2.1/z
    boundBoxHeight=(maxDiff(yCoordList))#*1.8/2.1/z
    return boundBoxHeight, boundBoxWidth
    #print("x:",x, "\nwidth:", boundBoxWidth,"\nHeight:",boundBoxHeight)
if __name__ == "__main__":
    main()