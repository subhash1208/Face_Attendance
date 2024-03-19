import os
import cv2
import face_recognition
import numpy as np
from datetime import datetime,date,timedelta

from Silent.test import test

test('images\Elon Musk.jpg','Silent-Face-Anti-Spoofing-master\resources\anti_spoof_models',0)
# finding images in the folder
path="images"
imaddrs=os.listdir(path)
#getting images and appeding in images list
images=[]
namesList=[]
for add in imaddrs:
    currentImage=cv2.imread(f'{path}/{add}')
    images.append(currentImage)
    # getting name without extension
    namesList.append(os.path.splitext(add)[0])
print("names in the database",namesList)

# posting attedance

def postAttedance(name):
    # maximum time require to post full attedance
    # 6hrs =21600 sec
    maxTimeInSec=21600
    tDate=date.today()
    try :
        f=open(f'attedanceSheet\{tDate}.csv',"x")
        f.writelines(f'Name,InTime,OutTime\n')
    except:
        print("...")
        
    with open(f"attedanceSheet\{tDate}.csv","r+") as f:
        currentFile=f'attedanceSheet\{tDate}.csv'
        # read the list for duplicate values
        namesList=[]
        inTimeList=[]
        outTimeList=[]
        fileData=f.readlines()
        for line in fileData:
            FileData=line.split(',')
            namesList.append(FileData[0])
            inTimeList.append(FileData[1])
            outTimeList.append(FileData[2])
# posting attedance if not present in the list
        if name not in namesList:
            now=datetime.now()
            dateTimeString=now.strftime('%H:%M:%S')
            f.writelines(f'{name},{dateTimeString},notAvailable\n')
            print("In time noted!")
            return 'In Time Noted'
        else:
            # find index of name in the list
            index=0
            for i in range(len(namesList)):
                if namesList[i]==name:
                    index=i
                    break
            # current date
            now=datetime.now()
            currentTime=now.strftime('%H:%M:%S')
            currentTimeC=datetime.strptime(currentTime,'%H:%M:%S')
            inTime=datetime.strptime(inTimeList[index],'%H:%M:%S')
            # checking if the user is out or not
            if outTimeList[index]=="notAvailable" or outTimeList[index]=="notAvailable\n" :
                timeDiff=(currentTimeC-inTime).total_seconds()
                if timeDiff>=60:
                    changeName,changeInTime,changeOutTime=fileData[index].split(',')
                    #changing out time
                    changeOutTime=currentTime
                    fileData[index]=changeName+','+changeInTime+','+changeOutTime+'\n'
                #in efficent code writes all lines in the file once again
                    file=open(currentFile,'w')
                    file.writelines(fileData)
                    print("Out time noted!")
                    return 'Out Time Noted'
                else:
                    print("in time noted",timeDiff,"seconds ago!")
                    return f'in time noted",{timeDiff},"seconds ago!'
            else:
                print("attedance already posted!")
                return "attedance already posted!"
    f.close()

# encoding images
def encode(images):
    encodedList=[]
    for img in images:
        converted=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        endoded=face_recognition.face_encodings(converted)[0]
        encodedList.append(endoded)
    return encodedList

listOfKnownEncodings=encode(images)
print("Encoding completed\n",len(listOfKnownEncodings),"faces in the list")


# starting the camera
cap=cv2.VideoCapture(0)
while True:
    status,frame=cap.read()
    #resizing the camera feed to reduce time
    smallImg=cv2.resize(frame,(0,0),None,0.25,0.25)
    #finding face locations in the frame
    currentFaceLoc=face_recognition.face_locations(smallImg)
    #encoding the images using locations in the frame
    currentEncode=face_recognition.face_encodings(smallImg,currentFaceLoc)
    #finding the face in known list of images
    for faceEncode,faceLoc in zip(currentEncode,currentFaceLoc):
        matches=face_recognition.compare_faces(listOfKnownEncodings,faceEncode)
        faceDis=face_recognition.face_distance(listOfKnownEncodings,faceEncode)
        print(faceDis)
        #finding the name from known list
        matchIndex=np.argmin(faceDis)
         # if match index matches the face print and show the face on the display
        if matches[matchIndex]:
            name=namesList[matchIndex]
            print(name)
            # we downscalled the image so locations are also downscaled
            #to upscale multiply coordinates with 4
            y1,x2,y2,x1=faceLoc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            #displaying a rectangle
            feedback=postAttedance(name)
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,225,0),2)
            cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,225,0),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.putText(frame,feedback,(4,30),cv2.FONT_HERSHEY_PLAIN,1,(0,0,225),2)

    # displaying the feed from the camera
    cv2.imshow("camera output",frame)
    cv2.waitKey(1)
