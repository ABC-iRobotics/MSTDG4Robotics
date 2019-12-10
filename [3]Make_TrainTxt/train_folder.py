import os

path='data/obj/'



imgList=os.listdir('obj')

print(imgList)

textFile=open('train.txt','w')


for img in imgList:
    imgPath=path+ img +'\n'
    textFile.write(imgPath)
