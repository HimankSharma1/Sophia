from tkinter import *
from PIL import Image, ImageTk
import pyttsx3
import time
import os
import speech_recognition
from threading import Thread
import datetime
import SophiaYt
import SophiaAddLocation

engine=pyttsx3.init('sapi5')
voices=engine.getProperty("voices")

class MainWindow:
    def StartTheWindow(self, geometry, title, win_bg, resizable=False):
        def Start():
            self.root=Tk()
            self.root.geometry(geometry)
            self.root.resizable(resizable, resizable)
            self.root.title(title)
            self.root.iconbitmap('icon.ico')
            self.root.config(bg=win_bg)
            self.iconFrame=Frame(self.root, height=590, width=260, background="black", bd=50).pack(side=LEFT, padx=3, pady=4)
            self.icon=Image.open("icon.jpg")
            self.icon=ImageTk.PhotoImage(self.icon)
            Label(self.iconFrame, text="Sophia,", bg="black", fg='#3AA8EC', font=("Times", 20)).place(x=10,y=300,)
            Label(self.iconFrame, text="Your Assistant on", bg="black", fg='#3AA8EC', font=("Times", 20)).place(x=10,y=333,)
            Label(self.iconFrame, text="duty", bg="black", fg='#3AA8EC', font=("Times", 20)).place(x=180,y=366)
            Label(self.iconFrame, image=self.icon, border=0).place(x=8,y=30)
            self.scrollbar=Scrollbar(self.root)
            self.outPut=Text(self.root, height=590, width=550, bg="black", font=("Times", 12), cursor='arrow', fg= 'light green')
            self.outPut.config(yscrollcommand=self.scrollbar.set, state="disable")
            self.scrollbar.config(command=self.outPut.yview)
            self.scrollbar.pack(side=RIGHT,fill=Y)
            self.outPut.pack(side=RIGHT, padx=3,pady=4)
            self.date=Label(self.root, font=("Times", 15), bg="black", fg='yellow', text=str(datetime.date.today().strftime("%d-%b-%Y")))
            self.date.place(x=16, y=450)
            self.my_menu=Menu(self.root)
            self.root.config(menu=self.my_menu)
            def CleanTheWin():
                self.outPut.config(state='normal')
                self.outPut.delete(1.0,'end')
                self.outPut.config(state='disable')

            self.my_menu.add_command(label="Clear", command=CleanTheWin)            

            self.location=Menu(self.my_menu, tearoff=0)
            self.my_menu.add_cascade(label="Location", menu=self.location)
            self.location.add_command(label="Change Directory", command=SophiaAddLocation.ChangeLocation)
            self.location.add_command(label="Open Directory", command=SophiaAddLocation.openLocation)
            self.yt=Menu(self.my_menu)
            self.my_menu.add_command(label="YtDownloader", command=SophiaYt.yt)

            def sql():
                import SophiaAddMysql
                SophiaAddMysql.add(False)
            self.database=Menu(self.my_menu, tearoff=0)
            self.my_menu.add_cascade(label="DataBase", menu=self.database)
            self.database.add_command(label="Add MySQL", command=sql)
            from SophiaManageDBMS import deleteContact
            self.database.add_command(label="Delete Contact", command=deleteContact)

            self.AddData=Menu(self.my_menu, tearoff=0)
            self.my_menu.add_cascade(label="Keywords", menu=self.AddData)
            from SophiaManageDBMS import add_file, add_link, delete_file, delete_web
            self.AddData.add_command(label="Add System File", command=add_file)
            self.AddData.add_command(label="Add Web URL", command=add_link)
            self.AddData.add_command(label="Delete System Keyword", command=delete_file)
            self.AddData.add_command(label="Delete Web Keyword", command=delete_web)

            from Screen_Recorder import rec_function
            self.my_menu.add_command(label="Screen Capture", command=rec_function)   

            def out2(text, say=True, output=True):
                if say == True:
                    Thread(target=speak, args=(text,)).start()
                elif say == False:
                    pass

                if output==True:
                    self.outPut.config(state='normal')
                    self.outPut.insert(0.0, text+'\n\n')
                    self.outPut.config(state='disable')
                elif output==False:
                    pass

            def Activate():
                text="First Press the F2 key and wait for the beep sound. After listening the beep sound tell your command."
                out2(text)
            
            def mysql():
                text="Select the Add MySQL from the 'Database' menu present in menu bar, and make the confermation. After confermation enter the MySQL details. Make sure to restart the program To apply changes"
                out2(text)

            def upload():
                text="To Upload the contacts in database, first activate the Assistant and speak 'Upload the Contacts' or 'Save the Contacts', and select the excel file. In the first column of first row write 'Name', and second column of first row write 'Phone', and store the data in respected columns in the excel file. Make sure to write the contact without country dialing code."
                out2(text)

            def delcontects():
                text="To delete the contacts from the database, select the 'Delete The Contact' from the 'Database' menu, a window will popup, and in the entry write the contact name."
                out2(text)
            
            def safety():
                text="The Developer of the program write the program in such a way so that all the data is stored in your local machine and your MySQL Server. You should not worry about the safety, we ensure you that all your data is not visible anywhere, even to the developer."
                out2(text)

            def searchgoogle():
                text="To make Google searches first activate the assistant, and speak 'search', and what to search. Example 'Search what is python language'"
                out2(text)

            def addkey():
                text="You can store two type of keywords. First is for System files and second is for browser links. If the keyword exist in the same type it will be replaced by the new one. if the same keyword is availabe in the another type it will replay 'Keyword reserved'. You can choose the type of keyword from the 'Keywords' menu present in menu bar."
                out2(text)
            
            def delkey():
                text="To delete the keyword, select the type of keyword to delete from the 'Keyword' menu present in the menu bar. And enter the keyword"
                out2(text)

            def whatmsg():
                text="To make a whatsapp message speak 'make a whatsapp message to (contact name availabe in database)'. After the beep sound speak your message. Make sure not to close the whatsapp window opened by the program in browser."
                out2(text)

            def playcont():
                text="To play a video on youtube speak 'play (your content)'. Example 'play lovely song'."
                out2(text)

            def locate():
                text="To Change or open the default Location, select a specific option as per your requirment from the 'Location' menu present in menu bar. After changing the directory Make sure to restart the program to Apply changes."
                out2(text)
        
            def seecont():
                text="To see The stored contacts in Database, speak 'show contacts' or 'show phone numbers'."
                out2(text)

            def seekey():
                text="To see The stored Keywords in Database, speak 'show Keywords'."
                out2(text)


            self.help=Menu(self.my_menu, tearoff=0)
            self.my_menu.add_cascade(label="Help", menu=self.help)
            self.help.add_command(label="How To Activate The Assistant?", command=Activate)
            self.help.add_separator()
            self.help.add_command(label="How To Change MySql Server?", command=mysql)
            self.help.add_separator()
            self.help.add_command(label="How To Upload Contacts?", command=upload)
            self.help.add_command(label="How To See The Stored Contacts in Database", command=seecont)
            self.help.add_command(label="How To Delete Contacts?", command=delcontects)
            self.help.add_command(label="Is it Safe To Upload Contacts or Add MySQL?", command=safety)
            self.help.add_separator()
            self.help.add_command(label="How To To Add KeyWords?", command=addkey)
            self.help.add_command(label="How To See The Stored Keywords in Database", command=seekey)
            self.help.add_command(label="How To To Delete KeyWords?", command=delkey)
            self.help.add_separator()
            self.help.add_command(label="How To Change or Open Media Files for the assistant Location?", command=locate)
            self.help.add_command(label="How To Make Google Searches?", command=searchgoogle)
            self.help.add_command(label="How To Make Whatsapp Messages?", command=whatmsg)
            self.help.add_command(label="How To Play Content on Youtube?", command=playcont)
            

            def dis():
                a=Thread(target=speak,args=("See you later",))
                a.start()
                self.root.destroy()
                time.sleep(1.5)
                os._exit(0)              
                
            self.root.protocol("WM_DELETE_WINDOW", dis)
            self.root.mainloop()
            
        Thread(target=Start).start()

    def out(self, text, say=True, output=True):
        if say == True:
            Thread(target=speak, args=(text,)).start()
        elif say == False:
            pass

        if output==True:
            self.outPut.config(state='normal')
            self.outPut.insert(0.0, text+'\n\n')
            self.outPut.config(state='disable')
        elif output==False:
            pass

def speak(audio):
    try:
        engine.endLoop()
    except:
        pass
    engine.say(audio)
    engine.runAndWait()

def SpeechRecognition(a=5):
    try:
        listener = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            listener.energy_threshold=280
            listener.operation_timeout=a
            voice = listener.listen(source, phrase_time_limit=a)
            command = listener.recognize_google(voice, language='en-us')            
            try:
                final = command.lower()
            except:
                pass
        return final
    except Exception as b:
        if b.__class__.__name__ == "RequestError":
            speak("Please connect to internet")
        elif b.__class__.__name__ == "UnknownValueError":
            speak("no input found")
        elif b.__class__.__name__ == "timeout":
            speak("Having unstable internet connection")

def ChangeVoice(index):
    engine.setProperty('voice', voices[index].id)
