import os
import cv2
import time
import glob
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)
first_frame = None

status_list = []
count = 1

def clean_folder():
    #to check threading procedure
    print("clean_folder fn started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean_folder fn ended")

while True:
    status = 0
    check,frame =video.read()

    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame_gau =  cv2.GaussianBlur(gray_frame,(21, 21), 0)

    if first_frame is None:
        first_frame=gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame,55,255,cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame,None, iterations=2)
    #cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours :
        if cv2.contourArea(contour) < 5000:
            continue

        #we know there is an object here
        x,y,w,h =  cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),3)

        if rectangle.any():
            status = 1 #when object enters the view
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images)/2) #finding most appropriate image that has object in frame
            image_with_obj = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        #this fn send_email() below requires time to be executed - causeing frames to freeze
        #can be solved by threading

        #preparing the threads - still needs calling of threads to execute
        email_thread = Thread(target=send_email, args=(image_with_obj, )) #making args=tuple
        email_thread.daemon = True #while frames are being displayed this is executed in the background
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()

        #cleaning folder after sending email
        #clean_folder()

    print(status_list)

    cv2.imshow("Video", frame)
    key=cv2.waitKey(1)

    if key==ord('q'):
        break
video.release()
clean_thread.start()
#delete images when user quits

