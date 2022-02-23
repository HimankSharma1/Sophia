from tkinter import messagebox
from tkinter import *
import SophiaWindow
import dotenv
class AddVoices:
    def __init__(self):
        Voices=SophiaWindow.voices[0:5]

        def SetButton(button, i):
            def SetVoice():
                global voice
                setbut.config(state="normal")
                SophiaWindow.engine.setProperty("voice", Voices[i].id)
                SophiaWindow.speak(f'It is the preview of the voice {i+1}')
                voice=i
                setbut.config(text=f"Set Voice-{i+1} as default voice", font=("TImes", 20, "italic"))
            button=Button(self.root, command=SetVoice, text=f"Press For The Preview Of Voice-{i+1}", fg="blue", font=("Times", 18, "italic")).place(x=160,y=200+(i*60))
        
        self.root=Tk()
        self.root.resizable(False, False)
        self.root.config(bg="#3AA8EC")
        self.root.geometry("650x673")
        self.root.iconbitmap('icon.ico')
        self.root.title("Voice Setup")
        
        frame=Frame(self.root, height=655, width=635, bg="black").place(x=7,y=10)
        frame2=Frame(self.root, height=490, width=400, bg="yellow").place(x=135,y=130)
        Label(frame, text="Please Setup The Voice", fg="yellow", bg='black', font=("Times", 35, "italic underline")).place(x=130,y=20)
        def dis():
            pass
        self.root.protocol("WM_DELETE_WINDOW", dis)
        def confirm():
            global voice
            Confirm=messagebox.askyesno("Confirm", f"Set Voice-{voice+1} as Default voice")
            if Confirm==True:
                self.root.destroy()
                with open(".env", "w") as EV:
                    pass
                dest=dotenv.find_dotenv()
                dotenv.set_key(dotenv_path=dest, key_to_set="Voice",  value_to_set=str(voice))
                SophiaWindow.speak('default voice set')


        setbut=Button(self.root, text=f"Click To set Default Voice",command=confirm, fg="red", font=("Times", 22, "italic"))
        setbut.config(state="disable")
        setbut.place(x=170, y=550)
        for i in range(len(Voices)):
            SetButton(f"But{i+1}", i)

        self.root.mainloop()
