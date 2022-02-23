from tkinter import Tk, filedialog
import dotenv
import SophiaWindow
import decouple
import os
import threading



def AddLocation():
    dest=dotenv.find_dotenv()
    threading.Thread(target=SophiaWindow.speak, args=("Please choose a default location for media files",)).start()

    a=Tk()
    a.withdraw()
    while True:
        fileLocation=filedialog.askdirectory(title="Set A Default Location", initialdir="D:")
        if fileLocation != "":
            dotenv.set_key(dotenv_path=dest, key_to_set="Location",  value_to_set=str(fileLocation))
            SophiaWindow.speak("Default Location set")
            a.destroy()
            break
        else:
            SophiaWindow.speak("Please Set a default location")
            continue
    a.mainloop()
    


def ChangeLocation():
    dest=dotenv.find_dotenv()

    a=Tk()
    a.withdraw()
    fileLocation=filedialog.askdirectory(title="Set A Default Location", initialdir="D:")
    if fileLocation != "":
        dotenv.set_key(dotenv_path=dest, key_to_set="Location",  value_to_set=str(fileLocation))
        a.destroy()
    else:
        a.destroy()
    
    a.mainloop()

def openLocation():
    location=decouple.config("Location")
    os.startfile(location)
    del location