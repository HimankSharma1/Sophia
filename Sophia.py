from threading import Thread
from decouple import config
import os

class FirstWin:
    def __init__(self):
        self.sound=pygame.mixer.Sound("welcome.mp3")
        self.sound.play()
        time.sleep(0.5)
        self.root=Tk()
        self.root.resizable(False,False)
        self.root.iconbitmap('icon.ico')
        self.root.geometry("1080x605+100+50")

        def disable():
            pass
        self.root.protocol("WM_DELETE_WINDOW", disable)
        self.root.title("Sophia Your Personal Assistant")
        self.image=Image.open("win.jpg")
        self.image=ImageTk.PhotoImage(self.image)
        Label(self.root, image=self.image).pack()
        Label(self.root, text="Sophia", bg="#13120E", fg="#D2D523", font=("Times", 35,"italic underline bold")).place(x=470, y=269)
        Label(self.root, text="Your Assistant on Duty",fg="#118CB5",bg="#242522", font=("Fixedsys", 30)).place(x=280,y=530)

        def StartTheProgram():
            self.root.destroy()
            self.sound=pygame.mixer.Sound("introduction.mp3")
            self.sound.play()
            time.sleep(12)
            import SophiaAddVoice
            SophiaAddVoice.AddVoices()
            import SophiaAddMysql
            SophiaAddMysql.AskYesNo()
            import SophiaAddLocation
            SophiaAddLocation.AddLocation() 
            from SophiaWindow import speak
            speak("Please start the program again")
            os._exit(0)     

        self.startbg=Image.open("startbut.jpg")
        self.startbg=ImageTk.PhotoImage(self.startbg)
        self.start_but=Button(self.root,image=self.startbg, borderwidth=0, border=0, command=StartTheProgram)
        self.start_but.place(x=20, y=150)

        def quit_win():
            os._exit(0)
        self.quitbg=Image.open("quitbut.jpg")
        self.quitbg=ImageTk.PhotoImage(self.quitbg)
        self.quit_but=Button(self.root,image=self.quitbg, borderwidth=0, border=0, command=quit_win)
        self.quit_but.place(x=865,y=150)
        self.root.mainloop()

if __name__=="__main__":
    try:
        with open(".env","r") as EV:
            pass
        import datetime
        from SophiaWindow import speak, ChangeVoice
        voice=int(config("Voice"))
        ChangeVoice(voice)
        import SophiaBackend
        
    except Exception as a:
        from tkinter import *
        from PIL import Image, ImageTk
        import os
        import pygame
        import time
        pygame.init()
        FirstWin() 
