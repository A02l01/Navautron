#! /usr/bin/python
import cv2
import sys
import time
import glob
import os
import smtplib
import serial



def light(instr):
	ser = serial.Serial('/dev/ttyACM0', 9600)
	if instr == 0:
		ser.write("0")
	if instr == 1:
		ser.write("1")
	

def send_mail(N,st):
	if st.find("Error")!=-1:
		fromaddr = 'phytotron.sclero@gmail.com'
		toaddrs  = 'barbacci@gmail.com'
		msg = 'Picture '+str(N)+' message '+str(st)


		# Credentials (if needed)
		username = 'phytotron.sclero@gmail.com'
		password = 'phyto.sclero'

		# The actual mail send
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(username,password)
		server.sendmail(fromaddr, toaddrs, msg)
		server.quit()

def get_last(path):
	try:
		newest = max(glob.iglob(path+'*.jpg'), key=os.path.getctime)
		return int((newest.split("/")[-1]).split(".jpg")[0])+1
	except ValueError:
		return -1
	
	
def write_log(st,path):
	f = open(path+"phyto.log",'a')
	f.write(st)
	f.close()

def mprint(v,stri):
	if v == True:
		print stri

def take_picture(path,N,save):
	for ii in range(0,5):
		print ii
		N = get_last(path+str(ii+1)+"/")
		st = str(N)+"\n"
			
		#video_capture = cv2.VideoCapture(ii)
		#video_capture.set(3,1280)
		#video_capture.set(4,780)
		#for j in range(0,500) :
		#	ret, frame = video_capture.read()
			#time.sleep(0.5)
		#if ret != False:
		#	video_capture.release()
		if save == "True":			
			pathb = path + str(ii+1)+"/"+str(N)+".jpg"
			print pathb
			#cv2.imwrite(pathb,frame)
			os.system("avconv -f video4linux2 -s 1920x1080 -i /dev/video"+str(ii)+" -ss 0:0:15 -frames 1 "+pathb)	
			st += pathb+" saved @ "
			st += time.ctime() +"\n"
		else :
			st += "Error \n"
	return st
	
if __name__=="__main__":
	print sys.argv
	instr = sys.argv[1]
	save  = sys.argv[2]
	path = "/home/phyto/Images/phyto/"
	#N = get_last(path+"1/")
	#if N != -1:
	#light(int(instr))
	st = take_picture(path,0,save)
	write_log(st,path)
	#send_mail(N,st)
	#light(0)
	#else:
	#	print("Prob")
		#send_mail(N,"Problem")
