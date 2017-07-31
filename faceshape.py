#importing the libraries
import numpy as np
import cv2
import dlib
from sklearn.cluster import KMeans

imagepath = "D:\workspace\FaceShape\i1.jpg"
# link = https://github.com/opencv/opencv/tree/master/data/haarcascades
cascade_path = "D:\workspace\FaceShape\haarcascade_frontalface_default.xml"
# download file path = http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
predictor_path = "D:\workspace\FaceShape\shape_predictor_68_face_landmarks.dat"

#create the haar cascade for detecting face
faceCascade = cv2.CascadeClassifier(cascade_path)

#create the landmark predictor
predictor = dlib.shape_predictor(predictor_path)

#read the image
image = cv2.imread(imagepath)

#for auto canny detection
v = np.median(image)
#resizing the image to 100 cols nd 50 rows
image = cv2.resize(image, (500, 500)) 

#convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#apply a Gaussian blur with a 3 x 3 kernel to help remove high frequency noise
gauss = cv2.GaussianBlur(gray,(3,3), 0)

#Detect faces in the image
faces = faceCascade.detectMultiScale(
    gauss,
    scaleFactor=1.05,
    minNeighbors=5,
    minSize=(100,100),
    flags=cv2.CASCADE_SCALE_IMAGE
    )

print("found {0} faces!".format(len(faces)) )

#looping through no of faces detected
for (x,y,w,h) in faces:
    #drawing 25% rectangle
    cv2.rectangle(image,(x,y), (x+w,y+int(0.25*h)), (0,255,100), 2 )
    #getting area of interest from image i.e., forehead
    forehead = image[y:y+int(0.25*h), x:x+w]

    cv2.imshow("forehead",forehead)
    rows,cols, bands = forehead.shape
    print('rows=',rows,'cols=',cols,'bands=',bands)
    X = forehead.reshape(rows*cols,bands)
    #kmeans.
    kmeans = KMeans(n_clusters=2,init='k-means++',max_iter=300,n_init=10, random_state=0)
    y_kmeans = kmeans.fit_predict(X)
    for i in range(0,rows):
        for j in range(0,cols):
            if y_kmeans[i*cols+j]==True:
                forehead[i][j]=[255,255,255]
            if y_kmeans[i*cols+j]==False:
                forehead[i][j]=[0,0,0]
                cv2.imshow('after',forehead)        
    #applying canny edge detection 
    #for more http://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    sigma = 0.33 #suggested value
    #compute the median of the single channel pixel intensities
    #v = np.median(image)
    #applying automatic canny edge detection using the computed median 
    lower = int(max(0,(1.0-sigma)*v))
    upper = int(min(255,(1.0+sigma)*v))
    edged = cv2.Canny(forehead,lower,upper)
    cv2.imshow("auto canny detection", edged)
    #draw a rectangle around the faces
    cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
    #converting the opencv rectangle coordinates to Dlib rectangle
    dlib_rect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
    print(dlib_rect)
    #detecting landmarks
    detected_landmarks = predictor(image, dlib_rect).parts()
    #converting to np matrix
    landmarks = np.matrix([[p.x,p.y] for p in detected_landmarks])
    #copying the image so we can we side by side
    original = image.copy()
    for idx, point in enumerate(landmarks):
            pos = (point[0,0], point[0,1] )
            #annotate the positions
            cv2.putText(original,str(idx),pos,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.4,color=(0,0,255) )
            #draw points on the landmark positions 
            cv2.circle(original, pos, 3, color=(0,255,255))

cv2.imshow("Faces found", image)
cv2.imshow("Landmarks found", original)




