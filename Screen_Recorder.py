from tkinter import *
import datetime
from PIL import ImageGrab
import numpy
import cv2
from win32api import GetSystemMetrics
import os
import threading
import decouple

voice=int(decouple.config("Voice"))
from SophiaWindow import speak
#trying to find the location of the default dir.....................


def rec_function():
    global destination, cam_recording, stop_no
    destination=decouple.config("Location")

    #two variable to know the status of webcam checkbox and stopping the rec...............
    stop_no=0
    cam_recording=0

    def cam():
    #function to check the status of the checkbox button................
        global cam_recording
        cam_recording +=1

    def stop():
    #function to check the status of the stop button..........
        global stop_no
        stop_no=1

    def disab():
    #disable the exit button while recording so the output must not be corrupted..........
        t2=threading.Thread(target=speak, args=['recording in process',])
        t2.start()

    def enable():
    #enable the exit button when the recording is no in process...............
        base.destroy()

    def start():
        t3=threading.Thread(target=speak, args=['recording',]).start()
        base.protocol("WM_DELETE_WINDOW", disab) 
        stopbutton.config(state='normal')
        startbutton.config(state='disabled')
        webcam.config(state='disabled')
        time_stamp=datetime.datetime.now().strftime('%y-%m-%d %H-%M-%S')
        name=f'{destination}/{time_stamp}.mp4' #name of the file which is to be save.......
        width=GetSystemMetrics(0)
        height=GetSystemMetrics(1)
        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        captured_vide0=cv2.VideoWriter(name, fourcc, 10.0,(width, height))
        if cam_recording%2!=0:
        #status of the webcam
            try:
                webcamera=cv2.VideoCapture(0)
            except:
                pass
        def lopstart():
            global stop_no
            while True:
                imag=ImageGrab.grab(bbox=(0,0,width,height))
                img_np=numpy.array(imag)
                if cam_recording%2!=0:
                    try:
                        _,frame=webcamera.read()
                        frame_height,frame_width,_=frame.shape
                        fh=height-frame_height
                        fw=width-frame_width
                    except:
                        pass
                img_final=cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                if cam_recording%2!=0:
                    try:
                        img_final[fh:height, fw:width, :]=frame[0:frame_height, 0:frame_width, :]
                    except:
                        pass
                captured_vide0.write(img_final)
                cv2.waitKey(1)
                if stop_no==1:
                    t4=threading.Thread(target=speak, args=['recording stopped']).start()
                    stopbutton.config(state='disabled')
                    webcam.config(state='normal')
                    startbutton.config(state='normal')
                    stop_no=0
                    break
            base.protocol("WM_DELETE_WINDOW", enable)
        t1=threading.Thread(target=lopstart)
        t1.start()

    def locate():
        os.startfile(destination)

    base=Tk()
    base.title('Screen Recorder')
    base.iconbitmap('icon.ico')
    base.resizable(False, False)
    base.geometry('500x150')
    base.config(bg='gray')
    webcam=Checkbutton(base, text='WebCam Recording', onvalue=1, offvalue=0, bg='gray', font=('Times',11), activebackground='gray', command=cam)
    webcam.place(x=20, y=50)
    startbutton=Button(base, text='Start', font=('Times', 20, 'bold'), bg='light green', command=start)
    stopbutton=Button(base, text='Stop', font=('Times', 20, 'bold'), bg='red', command=stop)
    locatebutton=Button(base, text='Location', font=('Times', 20, 'bold'), bg='sky blue', command=locate)
    stopbutton.place(x=270, y=37)
    stopbutton.config(state='disabled')
    startbutton.place(x=180,y=37)
    locatebutton.place(x=360,y=37)
    base.protocol("WM_DELETE_WINDOW", enable)
    base.mainloop()
