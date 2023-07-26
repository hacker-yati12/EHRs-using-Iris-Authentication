from flask import Flask, redirect, url_for, render_template, request
from IPython.display import HTML
from fnc.extractFeature import extractFeature
from fnc.matching import matching
from scipy.io import savemat
from time import time

import argparse, os
import scipy.io as sio
import cv2
import mysql.connector
import pandas as pd
import numpy as np

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="Abhi",
    password="abc123"
)
mycursor = mydb.cursor()
mycursor.execute("use med_hist")
mycursor.execute("select P_id from med_info")
myresult = mycursor.fetchall()
last=(max(myresult))
last_enroll=last[0]


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/medical_history")
def verify():
    if request.method == "GET":
        # #------------------------------------------------------------------------------
        # #	Argument parsing
        # #------------------------------------------------------------------------------
        # parser = argparse.ArgumentParser()

        # parser.add_argument("--file", type=str,default = ".\\test_iris.jpg",
        #                     help="Path to the file that you want to verify.")

        # parser.add_argument("--temp_dir", type=str, default=".\\templates\\temp\\",
        #                     help="Path to the directory containing templates.")

        # parser.add_argument("--thres", type=float, default=0.38,
        #                     help="Threshold for matching.")

        # args = parser.parse_args()


        # ##-----------------------------------------------------------------------------
        # ##  Execution
        # ##-----------------------------------------------------------------------------
        # # Extract feature
        # video=cv2.VideoCapture(0)
        # while True:
        #     ret,frame=video.read()
        #     cv2.rectangle(frame,pt1= (100,50),pt2 = (480,430),color = (0,255,0),thickness=5)

        #     cv2.imshow("iris image",frame)
        #     k = cv2.waitKey(1)
        #     if k == 13:
        #         test = (".\\test_iris.jpg")
        #         cv2.imwrite("img.jpg", frame)
        #         img = cv2.imread("img.jpg",0)
        #         img = img[50:430, 100:480]
        #         cv2.imwrite("test_iris.jpg", img)
        #         break

        # #release camera
        # video.release()

        # start = time()
        # print('>>> Start verifying {}\n'.format(args.file))
        # template, mask, file = extractFeature(args.file)


        # # Matching
        # result,match_dist = matching(template, mask, args.temp_dir, args.thres)
        # x= result.split(".")
        # if result == -1:
        #     print('>>> No registered sample.')

        # elif result == 0:
        #     print('>>> No sample matched.')

        # else:
        #     print(x[0])
        #     print("matching distance : ",match_dist)


        # # Time measure
        # end = time()
        # print('\n>>> Verification time: {} [s]\n'.format(end - start))
        
        # sql1 = "select * from med_hist.COLUMNS where TABLE_NAME='med_info' ;"
        sql1 = "show COLUMNS FROM Med_hist.med_info;"
        sql2 = "SELECT * FROM Med_info where P_id = 4;"
        mycursor.execute(sql1)
        mycol = mycursor.fetchall()
        mycursor.execute(sql2)
        myresult = mycursor.fetchall()

        html = """<style>
        @import "https://fonts.googleapis.com/css?family=Montserrat:300,400,700";
        body{
            text-align:center;
            background-color:rgb(87, 87, 87);
        }
        .rwd-table {
        margin: auto;
        min-width: 300px;
        }
        .rwd-table tr {
        border-top: 1px solid #ddd;
        border-bottom: 1px solid #ddd;
        }
        .rwd-table th {
        display: none;
        }
        .rwd-table td {
        display: block;
        }
        .rwd-table td:first-child {
        padding-top: .5em;
        }
        .rwd-table td:last-child {
        padding-bottom: .5em;
        }
        .rwd-table td:before {
        content: attr(data-th) ": ";
        font-weight: bold;
        width: 6.5em;
        display: inline-block;
        }
        @media (min-width: 480px) {
        .rwd-table td:before {
            display: none;
        }
        }
        .rwd-table th, .rwd-table td {
        text-align: left;
        }
        @media (min-width: 480px) {
        .rwd-table th, .rwd-table td {
            display: table-cell;
            padding: .25em .5em;
        }
        .rwd-table th:first-child, .rwd-table td:first-child {
            padding-left: 0;
        }
        .rwd-table th:last-child, .rwd-table td:last-child {
            padding-right: 0;
        }
        }

        h1 {
        # font-weight: normal;
        # letter-spacing: -1px;
        # color: #34495E;
        color:white;
        }

        .rwd-table {
        background: #34495E;
        color: #fff;
        border-radius: .4em;
        overflow: hidden;
        }
        .rwd-table tr {
        border-color: #46637f;
        }
        .rwd-table th, .rwd-table td {
        margin: .5em 1em;
        }
        @media (min-width: 480px) {
        .rwd-table th, .rwd-table td {
            padding: 1em !important;
        }
        }
        .rwd-table th, .rwd-table td:before {
        color: #dd5;
        }
        </style>
        <script>
        window.console = window.console || function(t) {};
        </script>
        <script>
        if (document.location.search.match(/type=embed/gi)) {
            window.parent.postMessage("resize", "*");
        }
        document.write("<h1>Your Medical History</h1>")
        </script>"""


        df = pd.DataFrame()
        df1 = pd.DataFrame()
        col=[]
        for x in mycol:
            col.append(x[0])
        
        df['Attributes'] = col
        for x in myresult:
            df3 = pd.DataFrame(list(x))
            df1 = pd.concat([df1,df3])
        df = pd.concat([df,df1],axis=1, join='inner')
        HTML(df.to_html('templates/sql-data.html'))
        with open("templates/sql-data.html") as file:
            file = file.read()
        file = file.replace("<table ", "<table class='rwd-table'")
        with open("templates/sql-data.html", "w") as file_to_write:
            file_to_write.write(html + file)
        # os.startfile("sql-data.html")

        
        # search for css insertion in the pandas library 
        # HTML(df.to_html(classes='table table-stripped'))
        return render_template("/sql-data.html")
 
@app.route("/registration", methods=["POST","GET"])
def registration():
    if request.method == "POST":
        name = request.form["name"]
        fname = request.form["fName"]
        email = request.form["email"]
        address = request.form["address"]
        adharNo = request.form["adhaar"]
        mobileNo = request.form["mobile"]
        gMobileNo = request.form["fMobile"]
        dob = request.form["DOB"]
        gender = request.form["gender"]
        query = ("insert into Med_info(name, F_name, Address, Adhaar, mob, alt_mob, email, DOB, Gender) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        mycursor.execute(query,(name,fname,address,adharNo,mobileNo,gMobileNo,email,dob,gender))
        mydb.commit()
        #------------------------------------------------------------------------------
        #	Argument parsing
        #------------------------------------------------------------------------------
        parser = argparse.ArgumentParser()

        parser.add_argument("--file", type=str,
                            help="Path to the file that you want to verify.")

        parser.add_argument("--temp_dir", type=str, default=".\\templates\\temp\\",
                            help="Path to the directory containing templates.")

        args = parser.parse_args()


        ##-----------------------------------------------------------------------------
        ##  Execution
        ##-----------------------------------------------------------------------------
        start = time()
        counter=last_enroll+1
        # counter=4;
        path = ".\sample\\"
        video=cv2.VideoCapture(0)
        while True:
            ret,frame=video.read()
            cv2.rectangle(frame,pt1= (100,50),pt2 = (480,430),color = (0,255,0),thickness=5)

            cv2.imshow("iris image",frame)
            k = cv2.waitKey(1)
            if k == 13:
                test = (str(counter) + ".jpg")
                cv2.imwrite(".\sample\\img.jpg", frame)
                img = cv2.imread(".\sample\\img.jpg",0)
                img = img[50:430, 100:480]
                cv2.imwrite(os.path.join(path+test), img)
                break

        #release camera
        video.release()   

        if not os.path.exists(args.temp_dir):
            print("makedirs", args.temp_dir)
            os.makedirs(args.temp_dir)
        args.file = ".\sample\\" + str(counter) + ".jpg"

        # Extract feature
        print('>>> Enroll for the file ', args.file)
        template, mask, file = extractFeature(args.file)

        # Save extracted feature
        basename = os.path.basename(file)
        out_file = os.path.join(args.temp_dir, "%s.mat" % (basename))
        savemat(out_file, mdict={'template':template, 'mask':mask})
        print('>>> Template is saved in %s' % (out_file))

        end = time()
        print('>>> Enrollment time: {} [s]\n'.format(end-start))

        return redirect("/medical_registration")
    else:
        return render_template("registration.html")
    
@app.route("/verification_choice",methods=["POST","GET"])
def verification_choice():
    if request.method=="POST":
        if request.form['submit']=='iris':
            # iris
            parser = argparse.ArgumentParser()

            parser.add_argument("--file", type=str,default = ".\\test_iris.jpg",
                                help="Path to the file that you want to verify.")

            parser.add_argument("--temp_dir", type=str, default=".\\templates\\temp\\",
                                help="Path to the directory containing templates.")

            parser.add_argument("--thres", type=float, default=0.38,
                                help="Threshold for matching.")

            args = parser.parse_args()


            ##-----------------------------------------------------------------------------
            ##  Execution
            ##-----------------------------------------------------------------------------
            # Extract feature

            video = cv2.VideoCapture(0)
            while True:
                ret,frame=video.read()
                cv2.rectangle(frame,pt1= (100,50),pt2 = (480,430),color = (0,255,0),thickness=5)

                cv2.imshow("iris image",frame)
                k = cv2.waitKey(1)
                if k == 13:
                    test = (".\\test_iris.jpg")
                    cv2.imwrite("img.jpg", frame)
                    img = cv2.imread("img.jpg",0)
                    img = img[50:430, 100:480]
                    cv2.imwrite("test_iris.jpg", img)
                    break

            #release camera
            video.release()

            start = time()
            print('>>> Start verifying {}\n'.format(args.file))
            template, mask, file = extractFeature(args.file)


            # Matching
            result,match_dist = matching(template, mask, args.temp_dir, args.thres)
            x= result.split(".")
            if result == -1:
                print('>>> No registered sample.')

            elif result == 0:
                print('>>> No sample matched.')

            else:
                print(x[0])
                print("matching distance : ",match_dist)


            # Time measure
            end = time()
            print('\n>>> Verification time: {} [s]\n'.format(end - start))
            return redirect("/medical_history")
        else:
            # fingerprint
            # open secind camera for fingerprint recognition
            cap = cv2.VideoCapture(0)                                   
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
            # crop = fingerprint_enhancer.enhance_Fingerprint(crop)
            # cv2.imshow('f_print',crop)

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
            return redirect("/medical_history")
    else:
        return render_template("verification_choice.html")

@app.route("/medical_registration",methods=["POST","GET"])
def medical_registration():
    if request.method == "POST":
        weight = request.form["Weight"]
        pulse = request.form["pulse"]
        bp = request.form["BP"]
        oxygen = request.form["oxygen level"]
        haemoglobin = request.form["haemoglobin"]
        platelets = request.form["PLT"]
        wbcCount = request.form["WBC"]
        hbsab = request.form["HBSAB"]
        hcv = request.form["HCV"]
        hiv = request.form["HIV"]
        ecg = request.form["ECG"]
        bloodSugar = request.form["blood sugar"]
        bloodUrea = request.form["blood urea"]
        Serum = request.form["serum creatinne"]
        albumin = request.form["albumin"]
        sugar = request.form["sugar"]
        ketone = request.form["ketone"]
        liver = request.form["liver"]
        spleen = request.form["spleen"]
        pancreas = request.form["pancreas"]
        kidney = request.form["kidney"]
        bacteria = request.form["bacteria"]
        cast = request.form["cast"]
        crystal = request.form["crystal"]
        pusCells = request.form["pus cells"]
        epithelialCells = request.form["epithelial cells"]
        RBCs = request.form["RBCs"]
        bloodGroup = request.form["blood group"]
        query = ("update Med_info set weight = %s,pulse_rate = %s, Blood_Pressure = %s, Oxygen_Level = %s, Haemoglobin = %s, Platelets = %s, Total_WBC_count = %s, HBSAG_Rapid_Card = %s, HCV_Rapid_Card = %s,HIV_I_and_HIV_II_Rapid_Card = %s,ECG = %s,Random_Blood_Sugar = %s,Blood_Urea = %s,Serum_Creatinne = %s,Albumin = %s,Sugar = %s,Ketone = %s,Liver = %s,Spleen = %s,Pancreas = %s,Kidneys = %s,Bacteria = %s,Cast = %s,Crystal = %s,Puscells = %s,Epithelialcells = %s,RBC_Count = %s,Blood_Group = %s where P_id = %s")
        mycursor.execute(query,(weight,pulse,bp,oxygen,haemoglobin,platelets,wbcCount,hbsab,hcv,hiv,ecg,bloodSugar,bloodUrea,Serum,albumin,sugar,ketone,liver,spleen,pancreas,kidney,bacteria,cast,crystal,pusCells,epithelialCells,RBCs,bloodGroup,last_enroll+1))
        mydb.commit()
        return redirect("/success")
    else:
        return render_template("medical_registration.html")

@app.route("/success",methods=["POST","GET"])
def success():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("success.html")
 
@app.route("/medical_history",methods=["POST","GET"])
def medical_history():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("sql-data.html")

if __name__ == "__main__":
    app.run(host="localhost",port=3000,debug=True)