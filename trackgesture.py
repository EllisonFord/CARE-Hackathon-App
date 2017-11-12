# -*- coding: utf-8 -*-
"""
    Created on Thu Mar  23 01:01:43 2017

    @author: abhisheksingh
    """

#%%
import sys
sys.path.append("this\is\the\path")
import pyparsing


import cv2
import numpy as np
import os
import time

import gestureCNN as myNN

from log_coms import *

global isDrinking

outputArray = [False,False,False,False]

# first element for drinking
# second element for smiling
# third element for sleeping
# fourth element for eating
# will be array of true and false


minValue = 70

x0 = 400
y0 = 200
height = 200
width = 200

saveImg = False
guessGesture = False
visualize = False

lastgesture = -1

kernel = np.ones((15,15),np.uint8)
kernel2 = np.ones((1,1),np.uint8)
skinkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

# Which mask mode to use BinaryMask or SkinMask (True|False)
binaryMode = True
counter = 0
# This parameter controls number of image samples to be taken PER gesture
numOfSamples = 301
gestname = ""
path = ""
mod = 0

banner =  '''\nWhat would you like to do ?
    1- Use pretrained model for gesture recognition & layer visualization
    2- Train the model (you will require image samples for training under .\imgfolder)
    3- Visualize feature maps of different layers of trained model
    '''


#%%
def saveROIImg(img):
    global counter, gestname, path, saveImg
    if counter > (numOfSamples - 1):
        # Reset the parameters
        saveImg = False
        gestname = ''
        counter = 0
        return

    counter = counter + 1
    name = gestname + str(counter)
    print("Saving img:",name)
    cv2.imwrite(path+name + ".png", img)
    time.sleep(0.04 )


#%%
def skinMask(frame, x0, y0, width, height ):
    global guessGesture, visualize, mod, lastgesture, saveImg
    # HSV values
    low_range = np.array([0, 50, 80])
    upper_range = np.array([30, 200, 255])

    cv2.rectangle(frame, (x0,y0),(x0+width,y0+height),(0,255,0),1)
    roi = frame[y0:y0+height, x0:x0+width]

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    #Apply skin color range
    mask = cv2.inRange(hsv, low_range, upper_range)

    mask = cv2.erode(mask, skinkernel, iterations = 1)
    mask = cv2.dilate(mask, skinkernel, iterations = 1)

    #blur
    mask = cv2.GaussianBlur(mask, (15,15), 1)
    #cv2.imshow("Blur", mask)

    #bitwise and mask original frame
    res = cv2.bitwise_and(roi, roi, mask = mask)
    # color to grayscale
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    if saveImg == True:
        saveROIImg(res)
    elif guessGesture == True:
        retgesture = myNN.guessGesture(mod, res)
        if lastgesture != retgesture :
            lastgesture = retgesture
            print myNN.output[lastgesture]
            time.sleep(0.01 )
    #guessGesture = False
    elif visualize == True:
        layer = int(raw_input("Enter which layer to visualize "))
        cv2.waitKey(0)
        myNN.visualizeLayers(mod, res, layer)
        visualize = False


    return res


#%%
def binaryMask(frame, x0, y0, width, height ):
    global guessGesture, visualize, mod, lastgesture, saveImg

    cv2.rectangle(frame, (x0,y0),(x0+width,y0+height),(0,255,0),1)
    roi = frame[y0:y0+height, x0:x0+width]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),2)
    #blur = cv2.bilateralFilter(roi,9,75,75)

    th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    ret, res = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #ret, res = cv2.threshold(blur, minValue, 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)

    if saveImg == True:
        saveROIImg(res)
    elif guessGesture == True:
        retgesture = myNN.guessGesture(mod, res)
        if lastgesture != retgesture :
            lastgesture = retgesture
            #print lastgesture

            ## Checking for only PUNCH gesture here
            ## Run this app in Prediction Mode and keep Chrome browser on focus with Internet Off
            ## And have fun :) with Dino
            if lastgesture == 3:
                jump = ''' osascript -e 'tell application "System Events" to key code 49' '''
                #jump = ''' osascript -e 'tell application "System Events" to key down (49)' '''
                os.system(jump)
                print myNN.output[lastgesture] + "= Dino JUMP!"

#time.sleep(0.01 )
#guessGesture = False
    elif visualize == True:
        layer = int(raw_input("Enter which layer to visualize "))
        cv2.waitKey(1)
        myNN.visualizeLayers(mod, res, layer)
        visualize = False

    return res

# For face
def faceRecognized(faces):
    try:
        if not faces:
            return False
        else: return True
    except:
        return True

savedTime = 0

def isDrinking(faceGone):
    global savedTime
    if (not faceGone):
        savedTime = time.time()  # if the face is seen
    else:
        newTime = time.time()
        if ((newTime - savedTime) > 1.5):
            return True
        else:
            return False

drinkingTime_1 = time.time()
drinkingTime_2 = time.time()

def sendDrinking(isDrinking):
    # if smile has been seen within 5 seconds, return false
    global drinkingTime_1
    global drinkingTime_2

    if (isDrinking):
        drinkingTime_1 = time.time()  # smile has been seen
        if ((drinkingTime_1 - drinkingTime_2) < 15): return False
        drinkingTime_2 = drinkingTime_1
        return True


# for brightness (for sleeping)
def isSleeping(brightness):
    if (brightness < 60): # brightness ranges from 0 to 255
        return True
    else:
        return False



'''
def sendSleepMsg(isBright):
    # if smile has been seen within 5 seconds, return false

    if ((not isBright) and (lastSleepState != True)):
        return True
'''

# For Smile
def isSmiling(smile):
    try:
        if not smile:
            return False
        else:
            return True
    except:
        return True

smileTime_1 = time.time()
smileTime_2 = time.time()

def sendSmile(isSmiling):
    # if smile has been seen within 5 seconds, return false
    global smileTime_1
    global smileTime_2

    if (isSmiling):
        smileTime_1 = time.time()  # smile has been seen
        if ((smileTime_1 - smileTime_2) < 5): return False
        smileTime_2 = smileTime_1
        return True

def calculateBrightness(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv) # value = brightness

    return np.average(v)

#%%
def Main():
    global guessGesture, visualize, mod, binaryMode, x0, y0, width, height, saveImg, gestname, path
    quietMode = False

    font = cv2.FONT_HERSHEY_SIMPLEX
    size = 0.5
    fx = 10
    fy = 355
    fh = 18

    #Call CNN model loading callback
    '''
    while True:
        
        ans = int(raw_input( banner))
        if ans == 2:
            mod = myNN.loadCNN(-1)
            myNN.trainModel(mod)
            raw_input("Press any key to continue")
            break
        elif ans == 1:
            print "Will load default weight file"
            mod = myNN.loadCNN(0)
            break
        elif ans == 3:
            if not mod:
                w = int(raw_input("Which weight file to load (0 or 1)"))
                mod = myNN.loadCNN(w)
            else:
                print "Will load default weight file"

            img = int(raw_input("Image number "))
            layer = int(raw_input("Enter which layer to visualize "))
            myNN.visualizeLayers(mod, img, layer)
            raw_input("Press any key to continue")
            continue

        else:
            print "Get out of here!!!"
            return 0
        '''

# facial recognition

# cascade
    face_cascade = cv2.CascadeClassifier('/Users/yoonheeh/Downloads/opencv-3.3.1/data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/Users/yoonheeh/Downloads/opencv-3.3.1/data/haarcascades/haarcascade_eye.xml')
    smilePath = "/Users/yoonheeh/Downloads/opencv-3.3.1/data/haarcascades/haarcascade_smile.xml"
    smile_cascade = cv2.CascadeClassifier(smilePath)


    ## Grab camera input
    cap = cv2.VideoCapture(1)
    cv2.namedWindow('Original', cv2.WINDOW_NORMAL)

    # set rt size as 640x480
    ret = cap.set(3,640)
    ret = cap.set(4,480)

    while(True):
        ret, frame = cap.read()
        max_area = 0

        frame = cv2.flip(frame, 3)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        smile = False
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            smile = smile_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.7,
                    minNeighbors=17,
                    minSize=(20, 20)
                )


            for (ex, ey, ew, eh) in smile:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

        brightness = calculateBrightness(frame)

        faceGone = not faceRecognized(faces)

        global outputArray

        if (isSleeping(brightness)): # if sleeping msg was sent, don't send other msgs
            outputArray[SLEEPING] = True
            outputArray[DRINKING] = False
            outputArray[SMILING] = False
            outputArray[EATING] = False
        else :
            outputArray[DRINKING] = sendDrinking(isDrinking(faceGone))
            outputArray[SLEEPING] = False
            outputArray[SMILING] = sendSmile(isSmiling(smile))
            outputArray[EATING] = False

        #call for results
        testStatus(outputArray)


        cv2.imshow('Original', frame)
            # cv2.imshow('ROI', roi)

        # Keyboard inputs
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        '''
        if ret == True:
            if binaryMode == True:
                roi = binaryMask(frame, x0, y0, width, height)
            else:
                roi = skinMask(frame, x0, y0, width, height)

        cv2.putText(frame,'Options:',(fx,fy), font, 0.7,(0,255,0),2,1)
        cv2.putText(frame,'b - Toggle Binary/SkinMask',(fx,fy + fh), font, size,(0,255,0),1,1)
        cv2.putText(frame,'g - Toggle Prediction Mode',(fx,fy + 2*fh), font, size,(0,255,0),1,1)
        cv2.putText(frame,'q - Toggle Quiet Mode',(fx,fy + 3*fh), font, size,(0,255,0),1,1)
        cv2.putText(frame,'n - To enter name of new gesture folder',(fx,fy + 4*fh), font, size,(0,255,0),1,1)
        cv2.putText(frame,'s - To start capturing new gestures for training',(fx,fy + 5*fh), font, size,(0,255,0),1,1)
        cv2.putText(frame,'ESC - Exit',(fx,fy + 6*fh), font, size,(0,255,0),1,1)

        ## If enabled will stop updating the main openCV windows
        ## Way to reduce some processing power :)
        if not quietMode:
            cv2.imshow('Original',frame)
            cv2.imshow('ROI', roi)

        # Keyboard inputs
        key = cv2.waitKey(10) & 0xff

        ## Use Esc key to close the program
        if key == 27:
            break

        ## Use b key to toggle between binary threshold or skinmask based filters
        elif key == ord('b'):
            binaryMode = not binaryMode
            if binaryMode:
                print("Binary Threshold filter active")
            else:
                print("SkinMask filter active")

        ## Use g key to start gesture predictions via CNN
        elif key == ord('g'):
            guessGesture = not guessGesture
            print("Prediction Mode - {}".format(guessGesture))

        ## This option is not yet complete. So disabled for now
        ## Use v key to visualize layers
        #elif key == ord('v'):
        #    visualize = True

        ## Use i,j,k,l to adjust ROI window
        elif key == ord('i'):
            y0 = y0 - 5
        elif key == ord('k'):
            y0 = y0 + 5
        elif key == ord('j'):
            x0 = x0 - 5
        elif key == ord('l'):
            x0 = x0 + 5

        ## Quiet mode to hide gesture window
        elif key == ord('q'):
            quietMode = not quietMode
            print "Quiet Mode - {}".format(quietMode)

        ## Use s key to start/pause/resume taking snapshots
        ## numOfSamples controls number of snapshots to be taken PER gesture
        elif key == ord('s'):
            saveImg = not saveImg

            if gestname != '':
                saveImg = True
            else:
                print "Enter a gesture group name first, by pressing 'n'"
                saveImg = False

        ## Use n key to enter gesture name
        elif key == ord('n'):
            gestname = raw_input("Enter the gesture folder name: ")
            try:
                os.makedirs(gestname)
            except OSError as e:
                # if directory already present
                if e.errno != 17:
                    print 'Some issue while creating the directory named -' + gestname

            path = "./"+gestname+"/"

#elif key != 255:
#    print key
        '''

#Realse & destroy
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    Main()

