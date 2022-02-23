import mysql.connector as mysql
from decouple import config
from tkinter import *
from threading import Thread
from tkinter import filedialog
from pandas import read_excel
from SophiaAddMysql import speak


def CreateDB(data):
    ed = data.cursor()
    try:
        ed.execute("create database Sophia")
    except:
        pass
    ed.execute("use sophia")
    try:
        ed.execute("create table phone (name varchar(25) primary key, number varchar(13))")
    except:
        pass
    try:
        ed.execute("create table files (name varchar(30) primary key, file varchar(300))")
    except:
        pass
    try:
        ed.execute("create table web (name varchar(30) primary key, web varchar(300))")
    except:
        pass
        data.close()

def uploadContacts():
    host=config("Host")
    user=config("User")
    sql_password=config("SqlPassword")
    if host=="None" or user=="None" or sql_password=="None":
        speak("please add my s q l")
    else:
        
        host=config("Host")
        user=config("User")
        sql_password=config("SqlPassword")
        Thread(target=speak, args=("please choose a excel file",)).start()
        Tk().withdraw()
        filename=filedialog.askopenfilename(title="Add a Excel File", initialdir="D:",filetypes=[("Excel files", "*.xlsx")])
        if filename!="":
            filename=read_excel(filename)
        file_content=filename.to_dict()
        FirstTitle=["Name","name", "Names", "names"]
        secondTitle=["Phone", "Phones", "phone", "phones", "Numbers","numbers", "Number", "number"]
        keys=list(file_content.keys())
        if keys[0] in FirstTitle:
            Names=file_content[keys[0]]
        else:
            speak("Please Set a valid name title in file")
        if keys[1] in secondTitle:
            Phone=file_content[keys[1]]
        else:
            speak("Please Set a valid number title in file")
        try:
            data = mysql.connect(host = host, user = user, password = sql_password, database="Sophia")
            ed = data.cursor()
            for i in range(len(Names)):
                try:
                    ed.execute(f"insert into phone values('{Names[i]}', '{Phone[i]}')")
                except:
                    ed.execute(f"update phone set number='{Phone[i]}' where name='{Names[i]}'")           
                data.commit()
            speak("data uploaded")
            data.close()
        except Exception as err:
            if err.__class__.__name__=="DatabaseError":
                Thread(target=speak, args=("unable to connect to my s q l server. please add again",)).start()


def deleteContact():
    a=Tk()
    a.resizable(False, False)
    a.config(bg="black")
    a.geometry("300x200")
    a.title("Delete a contact")
    a.iconbitmap('icon.ico')
    Label(a, text="Enter The Name", fg="red", bg="black", font=("Times", 20, "bold underline")).place(x=50, y=20)
    entry=Entry(a, font=("Times", 16, "bold "), fg="red", width=25)
    entry.place(x=10, y=80)
    def deleteno(abc=0):
        name=entry.get()
        host=config("Host")
        user=config("User")
        sql_password=config("SqlPassword")
        try:
            data = mysql.connect(host = host, user = user, password = sql_password, database="Sophia")
            ed = data.cursor()
            ed.execute("select Name from phone")
            c=ed.fetchall()
            contact_name=[]
            delete=0
            for i in range(len(c)):
                contact_name.append(str(c[i][0]).lower())
            for i in contact_name:
                if i == name.lower():
                    ed.execute(f"delete from phone where name='{i}'")
                    delete=1
                    data.commit()
                    ed.execute(f"select name from phone")
                    count=ed.fetchall()
            if len(contact_name)==0:
                a.destroy()
                Thread(target=speak, args=('database empty for contacts',)).start()
            else:
                if delete==1:
                    Thread(target=speak, args=(f"contact deleted, {len(count)} contacts remaining in the database",)).start()
                    entry.delete(0,'end')
                elif delete==0:
                    Thread(target=speak, args=("contact not found",)).start()
        except Exception as err:
            if err.__class__.__name__=="DatabaseError":
                Thread(target=speak, args=("unable to connect to my s q l server. please add again",)).start()
    entry.bind("<Return>", deleteno)
    Button(a, text="Delete", fg="red", font=("Times", 15, "bold"), command=deleteno).place(x=100, y=120)
    a.mainloop()

def add_file():
    host=config("Host")
    user=config("User")
    sql_password=config("SqlPassword")
    addFile=Tk()
    addFile.resizable(False, False)
    addFile.iconbitmap('icon.ico')
    addFile.config(bg="black")
    addFile.geometry("400x300")
    addFile.title("Adding a Keyword to File")
    Label(addFile, text="Enter a keyword:", font=("Times", 25, "italic underline"), bg="black", fg="red").place(x=20, y=20)
    KeyWord=Entry(addFile, font=("Times", 17), width=30)
    KeyWord.place(x=40, y=80)
    def uploadFile():
        name=KeyWord.get()
        try:
            test = mysql.connect(host = host, user = user, password = sql_password, database="Sophia")
            e = test.cursor()
            e.execute("select Name from web")
            c=e.fetchall()
            file_name=[]
            res=0
            test.close()
            for i in range(len(c)):
                file_name.append(str(c[i][0]).lower())    
            for i in file_name:
                if i == name.lower():
                    Thread(target=speak, args=("Keyword already reserved",)).start()
                    res=1
                    break
        except Exception as err:
            if err.__class__.__name__=="DatabaseError":
                res=1
                Thread(target=speak, args=("unable to connect to my s q l server. please add again",)).start()
        if res==0:
            if name=="" or name == ' ':
                Thread(target=speak, args=("you can not leave the keyword empty",)).start()
                KeyWord.delete(0,'end')
            else:
                addFile.withdraw()
                filename=filedialog.askopenfilename(title="Add A File", initialdir="D:")
                addFile.destroy()
                if filename=="":
                    pass
                else:
                    try:
                        data = mysql.connect(host = host, user = user, password = sql_password, database="Sophia")
                        ed = data.cursor()
                        try:
                            ed.execute(f"insert into files values('{name}', '{filename}')")
                        except:
                            ed.execute(f"update files set file = '{filename}' where name='{name}'")
                        data.commit()
                        Thread(target=speak, args=("keyword added",)).start()
                        data.close()
                    except:
                        pass
        else:
            KeyWord.delete(0,'end')

    Button(addFile, text="Choose a File", font=("Times", 30, "bold"), fg="red", command=uploadFile).place(x=60, y=180)
    addFile.mainloop()

def add_link():
    host=config("Host")
    user=config("User")
    sql_password=config("SqlPassword")
    addFile=Tk()
    addFile.resizable(False, False)
    addFile.config(bg="black")
    addFile.iconbitmap('icon.ico')
    addFile.geometry("400x350")
    addFile.title("Adding a Keyword to File")
    Label(addFile, text="Enter a keyword:", font=("Times", 25, "italic underline"), bg="black", fg="red").place(x=20, y=20)
    KeyWord=Entry(addFile, font=("Times", 17), width=30)
    KeyWord.place(x=40, y=80)
    Label(addFile, text="Enter a URL:", font=("Times", 25, "italic underline"), bg="black", fg="red").place(x=20, y=120)
    link=Entry(addFile, font=("Times", 15), width=33)
    link.place(x=40, y=180)
    def uploadlink():
        name=KeyWord.get()
        web=link.get()
        try:
            test = mysql.connect(host = host, user = user, password = sql_password, database="Sophia")
            e = test.cursor()
            e.execute("select Name from files")
            c=e.fetchall()
            file_name=[]
            res=0
            test.close()
            for i in range(len(c)):
                file_name.append(str(c[i][0]).lower())    
            for i in file_name:
                if i == name.lower():
                    Thread(target=speak, args=("Keyword already reserved",)).start()
                    res=1
                    break
        except Exception as err:
            if err.__class__.__name__=="DatabaseError":
                res=1
                Thread(target=speak, args=("unable to connect to my s q l server. please add again",)).start()
        if res==0:
            if name == "" and web=="":
                Thread(target=speak, args=["please enter a valid keyword and url"]).start()
            elif name=="":
                Thread(target=speak, args=["please enter a valid keyword"]).start()
            elif web=="":
                Thread(target=speak, args=["please enter a valid url"]).start()
            else:
                addFile.destroy()
                try:
                    data = mysql.connect(host = host, user = user, password = sql_password, database="Sophia")
                    ed = data.cursor()
                    try:
                        ed.execute(f"insert into web values('{name}', '{web}')")
                    except:
                        ed.execute(f"update web set web = '{web}' where name='{name}'")
                    data.commit()
                    Thread(target=speak, args=("keyword added",)).start()
                    data.close()
                except:
                    pass
        else:
            KeyWord.delete(0,'end')
    Button(addFile, text="Add KeyWord", font=("Times", 25, "bold"), fg="red", command=uploadlink).place(x=60, y=240)
    addFile.mainloop()

def delete_file():
    a=Tk()
    a.resizable(False, False)
    a.config(bg="black")
    a.geometry("300x200")
    a.iconbitmap('icon.ico')
    a.title("Delete System keywords")
    Label(a, text="Enter The Keyword", fg="red", bg="black", font=("Times", 20, "bold underline")).place(x=50, y=20)
    entry=Entry(a, font=("Times", 16, "bold "), fg="red", width=25)
    entry.place(x=10, y=80)
    def deletefile(abc=0):
        name=entry.get()
        host=config("Host")
        user=config("User")
        sql_password=config("SqlPassword")
        try:
            data = mysql.connect(host = host, user = user, password = sql_password, database="Sophia")
            ed = data.cursor()
            ed.execute("select Name from files")
            c=ed.fetchall()
            files_name=[]
            delete=0
            for i in range(len(c)):
                files_name.append(str(c[i][0]).lower())
                for i in files_name:
                    if i == name.lower():
                        ed.execute(f"delete from files where name='{i}'")
                        delete=1
                        data.commit()
                        ed.execute(f"select name from files")
                        count=ed.fetchall()
            if len(files_name)==0:
                a.destroy()
                Thread(target=speak, args=('database empty for System keywords',)).start()
                
            else:
                if delete==1:
                    Thread(target=speak, args=(f"Keyword deleted, {len(count)} keyword for files remaining in the database",)).start()
                    entry.delete(0,'end')
                elif delete==0:
                    Thread(target=speak, args=("keyword not found",)).start()
        except Exception as err:
            if err.__class__.__name__=="DatabaseError":
                Thread(target=speak, args=("unable to connect to my s q l server. please add again",)).start()
    entry.bind("<Return>", deletefile)
    Button(a, text="Delete", fg="red", font=("Times", 15, "bold"), command=deletefile).place(x=100, y=120)
    a.mainloop()

def delete_web():
    a=Tk()
    a.resizable(False, False)
    a.config(bg="black")
    a.geometry("300x200")
    a.iconbitmap('icon.ico')
    a.title("Delete Web Keyword")
    Label(a, text="Enter The Keyword", fg="red", bg="black", font=("Times", 20, "bold underline")).place(x=50, y=20)
    entry=Entry(a, font=("Times", 16, "bold "), fg="red", width=25)
    entry.place(x=10, y=80)
    def deleteweb(abc=0):
        name=entry.get()
        host=config("Host")
        user=config("User")
        sql_password=config("SqlPassword")
        try:
            data = mysql.connect(host = host, user = user, password = sql_password, database="Sophia")
            ed = data.cursor()
            ed.execute("select Name from web")
            c=ed.fetchall()
            files_name=[]
            delete=0
            for i in range(len(c)):
                files_name.append(str(c[i][0]).lower())
                for i in files_name:
                    if i == name.lower():
                        ed.execute(f"delete from web where name='{i}'")
                        delete=1
                        data.commit()
                        ed.execute(f"select name from web")
                        count=ed.fetchall()
            if len(files_name)==0:
                a.destroy()
                Thread(target=speak, args=("database empty for web keywords",)).start()
                    
            else:
                if delete==1:
                    Thread(target=speak, args=(f"Keyword deleted,{len(count)} keyword for web remaining in the database",)).start()
                    entry.delete(0,'end')
                elif delete==0:
                    Thread(target=speak, args=("keyword not found",)).start()
        except Exception as err:
            if err.__class__.__name__=="DatabaseError":
                Thread(target=speak, args=("unable to connect to my s q l server. please add again",)).start()
    entry.bind("<Return>", deleteweb)
    Button(a, text="Delete", fg="red", font=("Times", 15, "bold"), command=deleteweb).place(x=100, y=120)
    a.mainloop()
