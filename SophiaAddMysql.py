from tkinter import *
from tkinter import messagebox
import mysql.connector as mysql
import pyttsx3
import threading 
import dotenv, decouple

voice=int(decouple.config("Voice"))
engine=pyttsx3.init()
voices=engine.getProperty("voices")
engine.setProperty("voice", voices[voice].id)

def speak(audio):
    try:
        engine.endLoop()
    except:
        pass
    engine.say(audio)

    engine.runAndWait()

def AskYesNo(first=True):

    a=threading.Thread(target=speak, args=("do you have my s q l",))
    def disab():
        pass
    ask=Tk()
    ask.title("Add MySQL")
    a.start()
    ask.resizable(False, False)
    ask.protocol("WM_DELETE_WINDOW", disab)
    ask.geometry("400x240+400+200")
    ask.iconbitmap('icon.ico')
    ask.config(bg="#32D411")
    Frame(ask, bg="black", height=230, width=390).place(x=5, y=5)
    Label(ask, text="Do you Have MySQL?", font=("Times", 25, "italic"), bg="black", fg="cyan").place(y=15, x=45)
    def YesSql():
        ask.destroy()
        threading.Thread(target=speak, args=("Please add my s q l details",)).start()
        def kill():
            host=host_en.get()
            user=user_en.get()
            sql_password=pass_en.get()

            def ere():
                host_en.delete(0,'end')
                user_en.delete(0,'end')
                pass_en.delete(0,'end')
        
            if  (host == "" or host == " ") and (user == "" or user == " ") and (sql_password == "" or sql_password == " "):
                threading.Thread(target=speak,args=['you can not leave the entries empty']).start()
            elif (host == "" or host == " ") and (user == "" or user == " "):
                threading.Thread(target=speak,args=['please enter a valid host and user']).start()
                ere()
            elif (user == "" or user == " ") and (sql_password == "" or sql_password == " "):
                threading.Thread(target=speak,args=['please enter a valid user and password']).start()
                ere()
            elif (sql_password == "" or sql_password == " ") and (host == "" or host == " "):
                threading.Thread(target=speak,args=['please enter a valid host and password']).start()
                ere()
            elif host == "" or host == " ":
                threading.Thread(target=speak,args=['please enter a valid host']).start()
                ere()
            elif user == "" or user == " ":
                threading.Thread(target=speak,args=['please enter a valid user']).start()
                ere()
            elif sql_password == "" or sql_password == " ":
                threading.Thread(target=speak,args=['please enter a valid password']).start()
                ere()
            
            else:
                try:
                    data = mysql.connect(host = host, user = user, password = sql_password)
                    if data.is_connected():
                        sql.destroy()
                        route=dotenv.find_dotenv()
                        speak("connection established! data access granted. i will create a database name sophia, to access all the functions of the program")
                        dotenv.set_key(key_to_set="Host", value_to_set=host, dotenv_path=route)
                        dotenv.set_key(key_to_set="User", value_to_set=user, dotenv_path=route)
                        dotenv.set_key(key_to_set="SqlPassword", value_to_set=sql_password, dotenv_path=route)
                        from SophiaManageDBMS import CreateDB
                        CreateDB(data)
                        data.close()
                except:
                    threading.Thread(target=speak,args=['unable to establish connection, please fill the entries carefully']).start()
                    pass_en.delete(0, 'end')
        def cancel():
            threading.Thread(target=speak,args=['do you want to skip']).start()
            mess=messagebox.askyesno('CANCLE','Do you want to skip the process?')
            if mess==True:
                sql.destroy()
                if first==True:
                    route=dotenv.find_dotenv()
                    dotenv.set_key(key_to_set="Host", value_to_set='None', dotenv_path=route)
                    dotenv.set_key(key_to_set="User", value_to_set='None', dotenv_path=route)
                    dotenv.set_key(key_to_set="SqlPassword", value_to_set='None', dotenv_path=route)
                elif first==False:
                    pass
            elif mess==False:
                host_en.delete(0,'end')
                user_en.delete(0,'end')
                pass_en.delete(0,'end') 
                threading.Thread(target=speak,args=['please enter the my s q l details']).start()        
        sql=Tk()
        sql.resizable(False,False)
        sql.geometry('700x500+210+25')
        sql.iconbitmap('icon.ico')
        sql.title("Adding MySQL")
        sql.config(bg="#32D411")
        Frame(sql, height=480, width=680, bg="black").place(x=10,y=10)
        Label(sql, text="Please Add MySQL", font=("Times", 35, "italic underline"), bg="black", fg="cyan").place(x=150, y=20 )
        Label(sql, text="Enter The Host:", font=("Times", 25," bold italic underline"), bg="black", fg="yellow").place(x=50, y=120)
        host_en=Entry(sql,font=("Comic Sans MS",17,), border=2, foreground="red", bg="white")
        host_en.place(x=350,y=130)
        Label(sql, text="Enter The User:", font=("Times", 25," bold italic underline"), bg="black", fg="yellow").place(x=50, y=200)
        user_en=Entry(sql,font=("Comic Sans MS",17,), border=2, foreground="red", bg="white")
        user_en.place(x=350,y=210)
        Label(sql, text="Enter The Password:", font=("Times", 25," bold italic underline"), bg="black", fg="yellow").place(x=50, y=280)
        pass_en=Entry(sql,font=("Comic Sans MS",17,), border=2, foreground="red", bg="white", show="*")
        pass_en.place(x=350,y=290)
        start_pro=lambda a: kill()
        
        pass_en.bind('<Return>', start_pro)
        sub_but=Button(sql, text="Submit The SQL Details",command=kill, font=("Times", 18,"bold")).place(x=70,y=390)
        cancel_but=Button(sql, text="Cancel The Process",command=cancel, font=("Times", 18,"bold")).place(x=400,y=390)
        sql.protocol("WM_DELETE_WINDOW", cancel)
        sql.mainloop()
    
    yes=Button(ask, text="Yes", bg="gray", fg="light green", font=("Times", 25, "underline"), command=YesSql).place(x=60, y=120)
    
    def NoSql():
        ask.destroy()  
        if first==True:  
            speak("you might not be able to access somefunction of the program, you can add my s q l any time")   
            route=dotenv.find_dotenv()  
            dotenv.set_key(key_to_set="Host", value_to_set='None', dotenv_path=route)
            dotenv.set_key(key_to_set="User", value_to_set='None', dotenv_path=route)
            dotenv.set_key(key_to_set="SqlPassword", value_to_set='None', dotenv_path=route)
        elif first==False:
            speak("canceling the process")
            pass
    
    no=Button(ask, text="No", bg="gray", fg="red", font=("Times", 25, "underline"), command=NoSql).place(x=265, y=120)
    ask.mainloop()

def add(arg):
    multi=threading.Thread(target=AskYesNo, args=(arg,))
    multi.start()
