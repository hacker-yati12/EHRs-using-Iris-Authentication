import cv2
import os
import numpy as np
import fingerprint_enhancer
import argparse
from os import listdir

# read input image
# sample=cv2.imread("database/109_1.tif")
sample = cv2.imread("SOCOFing/SOCOFing/Altered/Altered-Hard/150__M_Right_index_finger_Obl.BMP")
input_image1 = cv2.resize(sample, None,fx=2.5, fy=2.5)
cv2.imshow("input_image" , input_image1)
cv2.waitKey(0)

# converting img to gray scale_0
img = cv2.cvtColor(input_image1, cv2.COLOR_BGR2GRAY)
cv2.imshow('grey_image', img);						
cv2.waitKey(0)	

# enhance the fingerprint image					
out = fingerprint_enhancer.enhance_Fingerprint(img)		
cv2.imshow('enhanced_image', out);						
cv2.waitKey(0)

best_score = 0
filename = None
image = None
kp1 = None
kp2 = None
mp = None


#reading image for fingerprint matching
counter = 0
i=0
for file in [file for file in os.listdir("SOCOFing/SOCOFing/Real")][:1000]:
    if counter % 10 ==0:
        print(counter)
        print(file)
    counter += 1
    fingerprint_database_image = cv2.imread("SOCOFing/SOCOFing/Real/" + file )
    #scale invariant feature transform
    sift = cv2.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
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
    if len(match_points) / keypoints * 100 > best_score:
        best_score = len(match_points) / keypoints * 100
        filename = file
        image = fingerprint_database_image
        kp1 = keypoints_1
        kp2 = keypoints_2
        mp = match_points

print("\nFigerprint ID: " + str(filename)) 
print("\nFingerprint match accuracy: " + str(best_score))

# fingerprint_database_image = fingerprint_enhancer.enhance_Fingerprint(fingerprint_database_image)
		
result = cv2.drawMatches(sample, kp1, fingerprint_database_image, 
                                kp2, mp , None) 
result = cv2.resize(result, None, fx=4, fy=4)

cv2.imshow("Result", result)
cv2.waitKey(0) 
cv2.destroyAllWindows()
       