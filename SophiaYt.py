from pytube import YouTube
import pyttsx3
import time
from tkinter import *
import os
import threading
from decouple import config

engine=pyttsx3.init()
voices=engine.getProperty('voices')

class YtDownload:
    def __init__(self, geometry):
        try:
            location=config("Location")
            voice=int(config("Voice"))
            engine.setProperty('vocie', voices[voice].id)

        except:
            from SophiaAddLocation import AddLocation
            AddLocation()
        def speak(auido):
            try:
                engine.endLoop()
            except:
                pass
            engine.say(auido)
            engine.runAndWait()
        self.root=Tk()
        self.root.config(bg="black")
        self.root.title("Download Youtube Video")
        self.root.resizable(False,False)
        self.root.iconbitmap('icon.ico')
        self.root.geometry(geometry)
        self.VideoLink=Entry(self.root, border=4, font=("Times",15))
        Label(self.root, text='Youtube Videos',fg='red', bg='black', font=('Times', 25)).place(x=90,y=30)
        Label(self.root, text='(Enter The url)',fg='red', bg='black', font=('Times', 25)).place(x=110,y=70)
        self.VideoLink.place(x=25, y=120, height=40, width=350)
        
        def GetVideo(resolution, formet):
            try:
                link=self.VideoLink.get()
                link=YouTube(link)
                StartTime=time.time()
                self.root.destroy()
            
                if formet=='mp4':
                    threading.Thread(target=speak, args=(f"starting the download at {resolution} resolution",)).start()
                    print("ok")
                    DownloadFile=link.streams.filter(resolution=resolution).first().download(output_path=location, filename_prefix=resolution)
                
                elif formet=="mp3":
                    threading.Thread(target=speak, args=("downloading the audio file",)).start()
                    DownloadFile=link.streams.filter(only_audio=True).first().download(output_path=location)
                    base = os.path.splitext(DownloadFile)
                    newfile=f"{base[0]}.mp3"
                    os.path.realpath(DownloadFile)
                    os.rename(DownloadFile, newfile)

                EndTime=time.time()
                TimeTaken=str(EndTime-StartTime)
                TimeTaken=TimeTaken.split(".")
                speak(f"download completed! the time taken is {TimeTaken[0]} seconds")
                self.root.destroy()
            except Exception as a:
                print(a)
                if (a.__class__.__name__)=="FileExixtsError":
                    threading.Thread(target=speak, args=("File Already Exist",)).start()
                elif a.__class__.__name__=="RegexMatchError":
                    threading.Thread(target=speak, args=("PLease enter a valid url of the video",)).start()

        down_360=lambda : GetVideo('360p', 'mp4')
        down_720=lambda : GetVideo('720p', 'mp4')
        down_mp3=lambda : GetVideo('360p', 'mp3')


        self.but1=Button(self.root, text="360p", font=('Times', 20,'bold'), fg='red', border=3, command=down_360).place(x=50, y=200)
        self.but2=Button(self.root, text="720p", font=('Times', 20,'bold'), fg='red', border=3, command=down_720).place(x=250, y=200)
        self.but3=Button(self.root, text="Audio", font=('Times', 20,'bold'), fg='red', border=3, command=down_mp3).place(x=145, y=280)
        self.root.mainloop()

def yt():
    a=threading.Thread(target=YtDownload, args=("400x400",))
    a.start()
