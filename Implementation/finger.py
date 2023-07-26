import cv2
import fingerprint_enhancer
import numpy as np
import os


# open secind camera for fingerprint recognition
cap = cv2.VideoCapture(1)                                   
while True:
    ret, img = cap.read()
    cv2.rectangle(img,pt1= (280,180),pt2 = (380,330),color = (0,255,0),thickness=5)
    

    cv2.imshow('fingerprint',img)


    # taking screenshot for fingerprint recognition
    k = cv2.waitKey(1) & 0xFF
    if k == 13:
        test = "test_finger.png"
        cv2.imwrite(test, img)
        break


# release camera
cap.release()
cv2.destroyAllWindows()

#converting img to gray scale
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#sharpening img for fingerprint enhancement
kernel_sharpening = np.array([[-1,-1,-1], 
                            [-1,9,-1], 
                            [-1,-1,-1]])
img = cv2.filter2D(img, -1, kernel_sharpening)

#using gaussian adaptive threshold for fingerprint extraction
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,2)


#crop fingerprint from img
crop_img = th3[190:320, 280:380]
test = "test_finger1.bmp"
test2 = "final_finger.bmp"
crop = cv2.resize(crop_img, None, fx = 1.5, fy = 1.5, interpolation = cv2.INTER_CUBIC)
crop = fingerprint_enhancer.enhance_Fingerprint(crop)
cv2.imshow('f_print',crop)

#store the fingerprint in folder
cv2.imwrite(test, th3)
cv2.imwrite(test2, crop)

cv2.waitKey(0)
cv2.destroyAllWindows()


#reading image for fingerprint matching
image=cv2.imread("final_finger.bmp")
img_list = os.listdir("./sample/fingerprint")
print(img_list)
for res in img_list: 
    fingerprint_database_image = cv2.imread("./sample/fingerprint/" + res)


    #using sift algorithm for finding differents points
    sift = cv2.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(image, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_database_image, None)  

    # matching the points using flann based matcher
    matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), 
                dict()).knnMatch(descriptors_1, descriptors_2, k=2)
    match_points = []

    #comparing the match points
    for p, q in matches:
        if p.distance <= 0.1*q.distance:
            match_points.append(p)
            
    keypoints = 0
    #storing matched keypoints 
    if len(keypoints_1) <  len(keypoints_2):
        keypoints = len(keypoints_1)            
    else:
        keypoints = len(keypoints_2)


    #checking fingerprint accuracy 
    if (len(match_points) / keypoints * 100 >=25):
        print("Fingerprint matched \n Access Granted!!!!")
        x = res.split("_")
        print(x[0])
        break
        
else:
    #if fingerprint doesnot match 
    print("Fingerprint does not match.")
cv2.waitKey(0)
cv2.destroyAllWindows()