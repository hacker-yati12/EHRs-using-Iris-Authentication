##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import argparse, os
from time import time
from scipy.io import savemat
import scipy.io as sio
import cv2
import mysql.connector
from fnc.extractFeature import extractFeature



#------------------------------------------------------------------------------
#	Connecting database
#------------------------------------------------------------------------------
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="abhi",
  password="abc12345"
)

mycursor = mydb.cursor()
mycursor.execute("use Med_hist")
mycursor.execute("select P_id from med_info")
myresult = mycursor.fetchall()
last=(max(myresult))
last_enroll=last[0]

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
args.file = ".\sample\\2.jpg"

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


