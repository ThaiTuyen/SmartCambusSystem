#  python3 "/home/pi/mqtt_firebase/loraNetwork.py"

import tkinter as tk
from tkinter import ttk 
import tkinter
from tkinter import BOTH, LEFT, TOP,RIGHT,BOTTOM, Frame,messagebox,OptionMenu,StringVar
import numpy as np
import cv2
import PIL.Image, PIL.ImageTk
import time

import const as CONST
import SendToThinkSpeak as ThinkSpeak
import DataMaster as DataMaster

from threading import Thread
import _thread

import FingerMaster as Checkin

import serial
import sys
import random
sys.path[0:0] = [""]
import os
import os.path


# set pin of lora module
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
PinM0 = 27
PinM1 = 17
AUXPin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(PinM0, GPIO.OUT)
GPIO.setup(PinM1, GPIO.OUT)
GPIO.setup(AUXPin, GPIO.IN)
GPIO.output(PinM0, 0)    # M0 M1 = LOW 
GPIO.output(PinM1, 0)
# set pin of lora module



lora_chanel = CONST.Str_HUB_lora_chanel
endMessSymbol = CONST.Str_endMessSymbol
HUB_LORA_ID = CONST.Str_HUB_LORA_ID
ADDR_HW =  CONST.Str_ADDR_HW 
ADDR_LW =  CONST.Str_ADDR_LW 


receive_WARMessage = CONST.receive_WARMessage

pingQueue = list()

loraSerial = serial.Serial(  
   port='/dev/ttyAMA0',
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)
"""
lorasetup
"""



class App:
     def __init__(self, window, window_title, video_source=0):
         self.window = window
         self.window.title(window_title)
         self.video_source = video_source

         fm = Frame(window)
 
         tkinter.Label( fm,  text="Device Manage:" ).pack(side = TOP, anchor="w",pady=15)

         t = ToggledFrame(fm, text='Device 1:', relief="raised", borderwidth=1)
         t.pack(fill="x", pady=2, padx=2, side = TOP, anchor="nw")
         self.TempurateAir1 = ttk.Label(t.sub_frame, text='Temperature Air (*C ) : ' + str(CONST.Data[0]) )
         self.TempurateAir1.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.Humidity1 = ttk.Label(t.sub_frame, text='Humidity Air (%) : '+ str(CONST.Data[1]) )
         self.Humidity1.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.TemperatureMax1 = ttk.Label(t.sub_frame, text='Temperature 2 (*C ) : '+ str(CONST.Data[2]))
         self.TemperatureMax1.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.Peresure1 = ttk.Label(t.sub_frame, text='Peresure (bmp) : ' + str(CONST.Data[3]))
         self.Peresure1.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.CoGas1 = ttk.Label(t.sub_frame, text='CO Gas (...) : ' + str(CONST.Data[4]))
         self.CoGas1.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.SoundNoise1 = ttk.Label(t.sub_frame, text='Sound Noise (db) : ' + str(CONST.Data[5]) )
         self.SoundNoise1.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.Status1 = ttk.Label(t.sub_frame, text='Status : ' + str(CONST.StrStatus1) )
         self.Status1.pack(pady=2, padx=2, side = TOP, anchor="nw")

         t2 = ToggledFrame(fm, text='Device 2:', relief="raised", borderwidth=1)
         t2.pack(fill="x", pady=2, padx=2, side = TOP, anchor="w")

         self.TempurateAir2 = ttk.Label(t2.sub_frame, text='Temperature Air (*C ) : ' + str(CONST.Data2[0]) )
         self.TempurateAir2.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.Humidity2 =  ttk.Label(t2.sub_frame, text='Humidity Air (%) : '+ str(CONST.Data2[1]) )
         self.Humidity2.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.TemperatureMax2 = ttk.Label(t2.sub_frame, text='Temperature 2 (*C ) : '+ str(CONST.Data2[2]))
         self.TemperatureMax2.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.Pressure2 = ttk.Label(t2.sub_frame, text='Pressure (bmp) : ' + str(CONST.Data2[3]))
         self.Pressure2.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.CoGas2 = ttk.Label(t2.sub_frame, text='CO Gas (...) : ' + str(CONST.Data2[4]))
         self.CoGas2.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.SoundNoise2 = ttk.Label(t2.sub_frame, text='Sound Noise (db) : ' + str(CONST.Data2[5]) )
         self.SoundNoise2.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.Status2 = ttk.Label(t2.sub_frame, text='Status : ' + str(CONST.StrStatus2) )
         self.Status2.pack(pady=2, padx=2, side = TOP, anchor="nw")
         
         tkinter.Label( fm,  text="Finger Manage:" ).pack(side = TOP, anchor="w", pady=15)
         t3 = ToggledFrame(fm, text='Information Accept:', relief="raised", borderwidth=1)
         t3.pack(fill="x", pady=2, padx=2, side = TOP, anchor="w")

         self.NameText = ttk.Label(t3.sub_frame, text='Full Name:' )
         self.NameText.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.IDText = ttk.Label(t3.sub_frame, text='ID       : ')
         self.IDText.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.Position = ttk.Label(t3.sub_frame, text='Position  : ')
         self.Position.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.Parterment = ttk.Label(t3.sub_frame, text='Part :' )
         self.Parterment.pack(pady=2, padx=2, side = TOP, anchor="nw")

         
         self.btn_snapshot=tkinter.Button(fm, text="Add Finger", width=50, command=self.AndFinger)
         self.btn_snapshot.pack(side = TOP, anchor="w")

         fm.pack(side=LEFT, fill=BOTH, expand=True)

         # open video source (by default this will try to open the computer webcam)
         self.vid = MyVideoCapture(self.video_source)
         # Create a canvas that can fit the above video source size
         fm2 = Frame(window)
         tkinter.Label( fm2,  text="Video Manage:" ).pack(side = TOP, anchor="w") 
  
         self.var = StringVar(fm2)
         self.lst = ["Video Stream", "Face detection", "People Counting", "None"]
         self.var.set(self.lst[0]) # initial value
         option = OptionMenu(fm2, self.var,*self.lst )
         option.pack(side = TOP, anchor="w",padx= 2,pady= 2)
         self.canvas = tkinter.Canvas( fm2, width = self.vid.width, height = self.vid.height)
         self.canvas.pack( side = TOP,ipadx= 5,ipady=5,padx= 10,pady= 10, fill = "x" , expand=1,anchor="w" )
         
         tkinter.Label( fm2,  text="Time: " ).pack(side = TOP, anchor="w",)

         t4 = ToggledFrame(fm2, text='Information In/Out:', relief="raised", borderwidth=1)
         t4.pack(fill="x", pady=2, padx=2, side = TOP, anchor="w")

         self.NumberIn = ttk.Label(t4.sub_frame, text='Number In  : ' + str(CONST.Data[0]) )
         self.NumberIn.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.NumberOut = ttk.Label(t4.sub_frame, text='Number out : '+ str(CONST.Data[1]) )
         self.NumberOut.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.TimeIn = ttk.Label(t4.sub_frame, text='Last Time In : '+ str(CONST.Data[1]) )
         self.TimeIn.pack(pady=2, padx=2, side = TOP, anchor="nw")
         self.TimeOut = ttk.Label(t4.sub_frame, text='Last Time Out : '+ str(CONST.Data[1]) )
         self.TimeOut.pack(pady=2, padx=2, side = TOP, anchor="nw")

         tkinter.Button(fm2, text="Information",command=self.advance).pack(side = TOP, anchor="w")

         ttk.Label(fm2, text='Design by: GF Team - email: tuyenathai@gmail.com ').pack(pady=2, padx=2, side = TOP, anchor="e")

         fm2.pack(side=LEFT, padx=10,pady= 10)
         self.delay = 5
         self.update()

         self.window.mainloop() 

     def AndFinger(self):
         #response = tkinter.messagebox.askquestion("Simple Question", "Do you add finger?")
         #if response == 1 :
        #self.btn_snapshot.pack_forget()
        self.btn_snapshot.config(state="disabled")
        self.Fingerwindow = tk.Toplevel(self.window)
        self.Fingerwindow.title("FG-And Finger")
        display = tk.Label(self.Fingerwindow, text="Finger config, insert a new Information !")
        display.pack(side = TOP) 
        fmInformation  = Frame (self.Fingerwindow)

        L1 = tk.Label(fmInformation, text="User Name")
        L1.grid( row = 0)
        self.V1 = StringVar()
        self.E1 = tk.Entry(fmInformation, textvariable= self.V1, bd =5)
        self.E1.grid(row = 0, column=1)
        L2 = tk.Label(fmInformation, text="ID")
        L2.grid( row = 1)
        self.V2 = StringVar()
        self.E2 = tk.Entry(fmInformation, textvariable= self.V2,bd =5)
        self.E2.grid(row = 1, column=1)
        L3 = tk.Label(fmInformation, text="Position")
        L3.grid( row = 2)
        self.E3 = tk.Entry(fmInformation, bd =5)
        self.E3.grid(row = 2, column=1)
        L4 = tk.Label(fmInformation, text="Part")
        L4.grid( row = 3)
        self.V4 = StringVar()
        self.E4 = tk.Entry(fmInformation,textvariable= self.V4, bd =5)
        self.E4.grid(row = 3, column=1)
        fmInformation.pack(side=TOP, padx=5,pady= 5,anchor = "w")
        fmSaveButon  = Frame (self.Fingerwindow)
        tk.Button(fmSaveButon, text="Save",command=self.SaveInfomation).pack(side = LEFT, anchor="w",padx=2,pady= 2)
        tk.Button(fmSaveButon, text="Exit",command=self.ExitInfomation).pack(side = LEFT, anchor="w",padx=2,pady= 2)
        fmSaveButon.pack(side=TOP, padx=5,pady= 5,anchor="e")
        #self.Fingerwindow.mainloop()

     def SaveInfomation(self):
        self.Fingerwindow.destroy()
        DataSave = [self.V1.get(),self.V2.get(),self.V4.get()]
        DataMaster.WriteData(DataSave)
        #self.btn_snapshot.pack()
        self.btn_snapshot.config(state="normal")

     def ExitInfomation(self):
     	self.Fingerwindow.destroy()
     	#self.btn_snapshot.pack()  
     	self.btn_snapshot.config(state="normal")   	

     def advance(self):
         # Get a frame from the video source
         tkinter.messagebox.showinfo("Information", "System V1.0, using lora and checkin finger")

     def update(self):
         # Get a frame from the video source
         #print(self.lst.index(self.var.get()))
         ret, frame = self.vid.get_frame(self.lst.index(self.var.get()))
         self.TempurateAir1.config(text = 'Temperature Air (*C ) : ' + str(CONST.Data[0]) )
         self.TempurateAir2.config(text = 'Temperature Air (*C ) : ' + str(CONST.Data2[0]) )
         self.Humidity1.config(text='Humidity Air (%) : '+ str(CONST.Data[1]))
         self.Humidity2.config(text='Humidity Air (%) : '+ str(CONST.Data2[1]))
         self.TemperatureMax1.config(text='Temperature 2 (*C ) : '+ str(CONST.Data[2]))
         self.TemperatureMax2.config(text='Temperature 2 (*C ) : '+ str(CONST.Data2[2]))
         self.Peresure1.config(text='Pressure (bmp) : ' + str(CONST.Data[3]))
         self.Pressure2.config(text='Pressure (bmp) : ' + str(CONST.Data2[3]))
         self.CoGas1.config(text='CO Gas (...) : ' + str(CONST.Data[4]))
         self.CoGas2.config(text='CO Gas (...) : ' + str(CONST.Data2[4]))
         self.SoundNoise1.config(text='Sound Noise (db) : ' + str(CONST.Data[5]))
         self.SoundNoise2.config(text='Sound Noise (db) : ' + str(CONST.Data2[5]))
         self.Status1.config(text='Status : ' + str(CONST.StrStatus1))
         self.Status2.config(text='Status : ' + str(CONST.StrStatus2))
         if CONST.PositionAccess == True:
              DataMaster.ReadData(CONST.PositionNum)
              self.NameText.config(text='Full Name: '+ CONST.FingerData[0])
              self.IDText.config(text='ID : '+ CONST.FingerData[1])
              self.Position.config(text='Position : '+str(CONST.PositionNum))
              self.Parterment.config(text='Part :'+ CONST.FingerData[2])
              CONST.PositionAccess = False
         self.NumberIn.config(text='Number In  : '+ str(CONST.DataCheckIn[0]))
         self.NumberOut.config(text='Number out : '+ str(CONST.DataCheckIn[1]))
         self.TimeIn.config(text='Last Time In : Null')
         self.TimeOut.config(text='Last Time Out : Null')
 
         if ret:
             self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
             self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
         self.window.after(self.delay, self.update)

 


class MyVideoCapture:
     def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
         self.faceCascade = cv2.CascadeClassifier('/home/pi/FinalProject/FactoryGuard/Cascades/haarcascade_frontalface_default.xml')
 
     def get_frame(self,DataMode):
         if self.vid.isOpened():
         	ret, img = self.vid.read()
         	if ret:
         		if DataMode == 0:
         			return (ret, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
         		elif DataMode == 1:
         			img = cv2.flip(img, 1)
         			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         			faces = self.faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(20, 20))
         			for (x,y,w,h) in faces:
         				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
         				roi_gray = gray[y:y+h, x:x+w]
         				roi_color = img[y:y+h, x:x+w]
         			return (ret, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
         		else:
         			return (ret, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
         	else:
         		return (ret, None)
         else:
         	return (ret, None)

     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()
             
             
class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(1)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='-', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self.sub_frame.pack(fill="x", expand=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')




""""
Lora funtion
"""


def Get_data_Str():
    msg  = '&field1=%d&field2=%d&field3=%d&field4=%d&field5=%d&field6=%d' %(CONST.Data[0],CONST.Data[1],CONST.Data[2],CONST.Data[3],CONST.Data[4],CONST.Data[5])
    CheckWarning()
    return msg
    
def Get_data2_Str():
    msg  = '&field1=%d&field2=%d&field3=%d&field4=%d&field5=%d&field6=%d' %(CONST.Data2[0],CONST.Data2[1],CONST.Data2[2],CONST.Data2[3],CONST.Data2[4],CONST.Data2[5])
    CheckWarning()
    return msg
    
def parse_json_object(data, obj):
    prefix = "\"%s\":\"" % obj
    prefix2 = '\'%s\':' % obj
    data.find(prefix)
    if (data.find(prefix) != -1):        
        index_prefix = data.find(prefix)
        index1 = data.find('\"', (len(prefix) + index_prefix - 1)) + 1
        index2 = data.find('\"', index1)
        dataOUT = data[index1:index2]
        return dataOUT
    elif (data.find(prefix2) != -1):        
        index_prefix = data.find(prefix2)
        index1 = data.find('\'', (len(prefix2) + index_prefix - 1)) + 1
        index2 = data.find('\'', index1)
        dataOUT = data[index1:index2]
        return dataOUT
    else:
        return ''
        
def parse_json_Data(data):
    prefix = "," 
    data.find(prefix)
    i = 0 
    while (data.find(prefix) != -1):        
        index_prefix = data.find(prefix)
        index1 = data.find('\"', (len(prefix) + index_prefix - 1)) + 1
        index2 = data.find('\"', index1)
        dataOUT = data[index1:index2]
        data = data[index2:]
        CONST.Data[i]=int(dataOUT)
        print (CONST.Data[i])
        i = i + 1
        
    if (i >=5 ):
    	return True
    else:
    	return False

def parse_json_Data2(data):
    prefix = "," 
    data.find(prefix)
    i = 0 
    while (data.find(prefix) != -1):        
        index_prefix = data.find(prefix)
        index1 = data.find('\"', (len(prefix) + index_prefix - 1)) + 1
        index2 = data.find('\"', index1)
        dataOUT = data[index1:index2]
        data = data[index2:]
        CONST.Data2[i]=int(dataOUT)
        print (CONST.Data2[i])
        i = i + 1
        
    if (i >=5 ):
    	return True
    else:
    	return False
        
def parse_json_Add_device(data):
    prefix = "A:" 
    prefix2 = "I:" 
    data.find(prefix)
    if (data.find(prefix) != -1):        
        index_prefix = data.find(prefix)
        index1 = data.find('\"', (len(prefix) + index_prefix - 1)) + 1
        index2 = data.find('\"', index1)
        dataOUT = data[index1:index2]
        
        index_prefix = data.find(prefix2)
        index1 = data.find('\"', (len(prefix2) + index_prefix - 1)) + 1
        index2 = data.find('\"', index1)
        dataKEY = data[index1:index2]
        print (dataOUT)
        print (dataKEY)
        if dataKEY in CONST.KEYID_HUB:
            print("{\"ACCNFG\",\"" +dataOUT + "\"}")
            return True
        print(data)

    return False

def send_lora_mess(AH, AL, chan, mess):
    ADDR_H = AH
    ADDR_L = AL
    Lora_chanel = chan
    SendBuf =  ADDR_H + ADDR_L + Lora_chanel + HUB_LORA_ID + mess +  endMessSymbol
    print("SendBuf: %s\n" % SendBuf)    
    loraSerial.write(SendBuf.encode(encoding = 'cp855', errors='strict'))
    return
 
    
def receive_Lora_Message(buf):
    try:  
        LORA_Mess = buf
        print("LORA_Mess : %s\n" % LORA_Mess[2:])
        if "S:FG2301" in LORA_Mess or "S:FG2302" in LORA_Mess:
            if "S:FG2301" in LORA_Mess:
                if parse_json_Data(LORA_Mess):
                    print("Read Data1 done")
                    msg = Get_data_Str()
                    ThinkSpeak.ThingSpeak_admin_begin(msg)
            elif "S:FG2302" in LORA_Mess:
                if parse_json_Data2(LORA_Mess):
                    print("Read Data done")
                    msg = Get_data2_Str()
                    ThinkSpeak.ThingSpeak2_admin_begin(msg)
            else:
            	print("Read Data fail")
            return
            
        if "RECNWFG" in LORA_Mess:
            print("Add Devide")
            if parse_json_Add_device(LORA_Mess) :
                return
            return
        if "UNCNWFG" in LORA_Mess:
            print("Remove Devide")
            if parse_json_Add_device(LORA_Mess) :
                return
            return
        if "ACMESWAR" in LORA_Mess and  "12345" in LORA_Mess :
            receive_WARMessage = True
            return        
        return
    except:
        print("error when receive_Lora_Message(buf)")


def check_lora_mess_receive_Loop():
    while True:      
        if(loraSerial.inWaiting() > 0):
            print("ok")
            lora_mess = bytes()
            char = bytes()
            while True:
                char = loraSerial.read()
                lora_mess = lora_mess + char
                if (char == bytes.fromhex(CONST.endMessSymbol)):   
                    break      
            message = (lora_mess).decode(encoding = 'cp855', errors='strict')
            receive_Lora_Message(message)            
        time.sleep(0.1)

def SenWarning_lora():
    receive_WARMessage = False
    #while True:      
    send_lora_mess(ADDR_HW, ADDR_LW, lora_chanel, "{\"WARNING\",\"12345\"}")         
    time.sleep(3)
        #return
    """    if receive_WARMessage:
            print("send warning done ")
            break
        time.sleep(15)"""
        
def CheckWarning():
    if (CONST.Data[4] >1000 or CONST.Data2[4]>1000):
        SenWarning_lora()

def loraNetwork_begin():
    try:
        print("connecting to broker")
        _thread.start_new_thread(check_lora_mess_receive_Loop, ())
        #_thread.start_new_thread(SenWarning_lora, ())
    except:
        print ("Error: unable to start thread")

time.sleep(1)

loraNetwork_begin()
_thread.start_new_thread(Checkin.checkFinger, ())
App(tkinter.Tk(), "Factory Guard")
while 1:
    if KeyboardInterrupt:
        print ('Interrupted')
        GPIO.cleanup()
        sys.exit(0)
    pass



