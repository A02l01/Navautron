#!/usr/bin/python


################################################################################################

import time,sys,cv2
import glob,os,shutil
import pdb
import numpy as np
import matplotlib.pyplot as plt


def get_intrinsics(f):
	doc = open(f,'r')
	s = ""
	for l in doc.readlines():
		s+=l
	s = s[s.find("<data>"):s.find("</data>")]
	tab = s.split()
	INT = np.zeros((3,3))
	INT[0,0]=float(tab[1])
	INT[0,2]=float(tab[3])
	INT[1,1]=float(tab[5])
	INT[1,2]=float(tab[6])
	INT[2,2]=1
	return INT

def get_distortion(f):
	doc = open(f,'r')
	s = ""
	for l in doc.readlines():
		s+=l
	s = s[s.find("<data>"):s.find("</data>")]
	tab = s.split()
	INT = np.zeros((1,5))
	INT[0,0]=float(tab[1])
	INT[0,1]=float(tab[2])
	INT[0,2]=float(tab[3])
	INT[0,3]=float(tab[4])
	INT[0,4]=float(tab[5])
	return INT

path = os.getcwd()+'/'+sys.argv[1]+'/'
# path = "/media/ab/Zeus/Phyto/Ophelie_M2/Exp4"+'/'+sys.argv[1]+'/'
print("Calibration of "+path)

# Loading from xml files
intrinsic = get_intrinsics(path+"Intrinsics.xml")
distortion = get_distortion(path+"Distortion.xml")

print "loaded all distortion parameters"



for file in glob.glob(path+"*.jpg"):
	sys.stdout.write("\r%s" % file)
	sys.stdout.flush()
	image=cv2.imread(file)
	if not os.path.exists(path+"raw/"):
		   os.makedirs(path+"raw/")
	shutil.move(file,path+"raw/"+os.path.basename(file))

	h,  w = image.shape[:2]
	newcameramtx, roi=cv2.getOptimalNewCameraMatrix(intrinsic,distortion,(w,h),1,(2*w,2*h))

	mapx,mapy = cv2.initUndistortRectifyMap(intrinsic,distortion,None,newcameramtx,(2*w,2*h),5)
	dst = cv2.remap(image,mapx,mapy,cv2.INTER_LINEAR)
	# plt.imshow(dst)
	# plt.show()
	cv2.imwrite(file,dst)

###############################################################################################
