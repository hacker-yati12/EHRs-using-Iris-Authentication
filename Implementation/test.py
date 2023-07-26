import mysql.connector
import cv2
import pandas as pd
import numpy as np
import fingerprint_enhancer

# mydb = mysql.connector.connect(
#   host="127.0.0.1",
#   user="dhanush",
#   password="abc12345"
# )


# mycursor = mydb.cursor()

# # mycursor.execute("CREATE DATABASE mydatabase")

# mycursor.execute("use med_hist")
# # mycursor.execute(select * from med_info)
# mycursor.execute("select P_id from med_info")
# myresult = mycursor.fetchall()
# last=(max(myresult))
# print(last[0])
# name = 'abhi'
# F_name = "kldsjafj"
# Address = "uhadsi"
# Adhaar = "56565"

# query="insert into med_info (name, F_name, Address, Adhaar, mob, alt_mob, email, DOB, Gender ) values ('Abhi Kumar Singh', 'Kartik Kumar Singh', 'Patna Bihar', 954178863049, 7352283805, 8935905626, 'abhi24680@outlook.com', '2001-09-12', 'M')"
# query=("insert into med_info (name, F_name, Address, Adhaar) values (%s, %s, %s, %s)")
# mycursor.execute(query,(name,F_name,Address, Adhaar))
# mydb.commit()
# print(mycursor.lastrowid)
# last= mycursor.insert_id() 
# print(last)
# mycursor.execute("select P_id from med_info where P_id = last_insert_id()")
# myresult = mycursor.fetchall()
# print(myresult)
# print("1 record inserted, id:",mycursor.lastrowid)
# result="1.jpg"
# x=result.split(".")
# # print(x[0])
# min = (x[0])
# sql = ("SELECT * FROM Med_info where P_id = %s;")
# mycursor = mydb.cursor()
# mycursor.execute(sql, (min,))
# myresult = mycursor.fetchall()
# df = pd.DataFrame()
# for x in myresult:
#   print(myresult)
  # df2 = pd.DataFrame(list(x)).T
  # df = pd.concat([df,df2])


cap = cv2.VideoCapture(1)                                   
while True:
    ret, img = cap.read()
    cv2.rectangle(img,pt1= (280,180),pt2 = (380,330),color = (0,255,0),thickness=5)
    

    cv2.imshow('fingerprint',img)


    # taking screenshot for fingerprint recognition
    k = cv2.waitKey(1) & 0xFF
    if k == 13:
        test = "test_finger.jpg"
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
test2 = "final_finger.jpg"
crop = cv2.resize(crop_img, None, fx = 1.5, fy = 1.5, interpolation = cv2.INTER_CUBIC)
crop = fingerprint_enhancer.enhance_Fingerprint(crop)
cv2.imwrite("./sample//"+test2, crop)

cv2.waitKey(0)
cv2.destroyAllWindows()