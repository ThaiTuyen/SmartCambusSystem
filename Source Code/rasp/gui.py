import tkinter as tk
from tkinter import ttk
#from tkinter import*
import tkinter
from tkinter import BOTH, LEFT, TOP,RIGHT,BOTTOM, Frame,messagebox,OptionMenu,StringVar
import numpy as np
import cv2
import PIL.Image, PIL.ImageTk
import time
import const as CONST
import DataMaster as DataMaster

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
         t3 = ToggledFrame(fm, text='Information Accept: No Accept', relief="raised", borderwidth=1)
         t3.pack(fill="x", pady=2, padx=2, side = TOP, anchor="w")

         self.NameText = ttk.Label(t3.sub_frame, text='Full Name: not found ' )
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
         self.lst = ["Video Stream", "Face detection", "Face recognition", "None"]
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
         try:
         	ret, frame = self.vid.get_frame(self.lst.index(self.var.get()))
         	if ret:
         		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
         		self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
         except:
         	tkinter.messagebox.showerror("Warning", "System can't open camera")

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
         self.faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
 
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



App(tkinter.Tk(), "Factory Guard")
