from pymongo import MongoClient
import psycopg2
import os.path
import Query.calcYolo as yolo
import math

_BIN_HEIGHT = 0.43
trainFile_name = 'train.txt'
save_path = os.getcwd() + "\\image_yolo_set"

def Generate():
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["DeepLearningTrainingSet"]
    mycol = mydb["BinPicking"]
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
    try:
        calculate_and_create_text(objects_records, objects_headers, 'image_set\\','.jpg')
    except:
        print("ERROR: generateYoloData: Generation for YOLO data was FAILED")


def create_objects(results):
    '''
    Take the query outcome and convert to a list and return it.
    It also defines headers and return it.
    '''
    records = []
    headers = ['id','imageUrl','absolutePosition1', 'absolutePosition2', 'absolutePosition3', 'absoluteOrientation1','absoluteOrientation2','absoluteOrientation3','absoluteOrientation4','relativePosition1', 'relativePosition2', 'relativePosition3', 'relativeOrientation1','relativeOrientation2','relativeOrientation3','relativeOrientation4', 'size_x', 'size_y', 'size_z', 'visionSensor_z', 'table_z']
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
            try:
                tmp.append(str(position['size'][0]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['size'][1]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(position['size'][2]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(record['visionSensor']['absolutePosition'][2]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(record['visionSensor']['perspectiveAngle']))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(record['table']['absolutePosition'][2]))
            except IndexError:
                tmp.append('NA')
            try:
                tmp.append(str(record['table']['size'][2]))
            except IndexError:
                tmp.append('NA')
            records.append(tmp)
    return records, headers


def calculate_and_create_text(records, headers, beg, end):
    "DGU: Rotate the bounding boxes and print in the textes"
    temp=""
    tmp2=''
    file_name='NA'
    imageNames = ""
    for record in records:
        absPos = [float(record[2]), float(record[3]), float(record[4])]
        absOrientation = [float(record[5]), float(record[6]), float(record[7]), float(record[8])]
        relPos = [float(record[9]), float(record[10]), float(record[11])]
        relOrientation = [float(record[12]), float(record[13]), float(record[14]), float(record[15])]
        objSize = [float(record[16]), float(record[17]), float(record[18])]
        visionSensorPosHeight = float(record[19])
        visionSensorAngle = float(record[20])
        tablePosHeight = float(record[21])
        tableHeight = float(record[22])
        # print("absOrientation:", absOrientation)
        # print("relPos:", relPos)
        # print("objSize:", objSize)
        # print("visionSensorPosHeight:", visionSensorPosHeight)
        # print("visionSensorAngle:", visionSensorAngle)
        # print("tablePosHeight:", tablePosHeight)
        # print("tableHeight:", tableHeight)
        #Calculate the central point on YOLO image
        absHeight = visionSensorPosHeight - tablePosHeight - tableHeight/2
        #print("absHeight", absHeight)
        absWidth = absHeight*math.tan(visionSensorAngle/2)*2
        #print("visionSensorPosHeight", visionSensorPosHeight)
        #print("absWidth", absWidth)

    #Calculate central point and bounding box size
        midX=(relPos[0]*absHeight)/((relPos[2])*(-absWidth)) + 0.5
        midY=((relPos[1] * absHeight) / (relPos[2] * (absWidth))) + 0.5
        boundingBoxSize =yolo.rotBoundBox (absOrientation, relPos, objSize, absHeight, absWidth)

    #Determine whether the object orientation is OE or 3O
        OEClass = yolo.GetObjectTopSurface(absOrientation) # 0: 3O, 1:OE
        #print("OE details: ", OEClass, midX, midY, boundingBoxSize)
        isInBin = yolo.IsInBin(absPos[2])

    #Write the object YOLO details into each text file
        if record[1]==tmp2:
            if isInBin:
                temp=temp + str(OEClass) + " " + str(midX) +" " + str(midY) + " " + str(boundingBoxSize[0]) + " " + str(boundingBoxSize[1]) + str('\n')
        elif file_name != 'NA':
            temp=temp.replace("[","").replace("]","").replace("'","").replace(",","")
            completeName = os.path.join(save_path, file_name)
            f = open(completeName, 'w', encoding='utf-8')
            f.write(str(temp))
            f.close()
            imageNames = imageNames + "data/obj/" + find_between(record[1], beg, end) + ".jpg\n"
            if isInBin:
                temp = str(OEClass) + " " + str(midX) + " " + str(midY) + " " + str(boundingBoxSize[0]) + " " + str(
                    boundingBoxSize[1]) + str('\n')
            else:
                temp = ""
        else:
            if isInBin:
                temp = str(OEClass) + " "+ str(midX) + " " + str(midY) + " " + str(boundingBoxSize[0]) + " " + str(
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
    print("generateYoloData: Training data for YOLO was generated")

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""