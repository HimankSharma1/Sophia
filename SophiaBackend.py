from SophiaAddMysql import speak
import SophiaWindow
import SophiaYt
import keyboard
import time, datetime
import wikipedia
import webbrowser, os 
import requests
from decouple import config
import pygame
import mysql.connector as mp

pygame.init()
sound=pygame.mixer.Sound("Activation beep.wav")
audio=int(config("Voice"))
SophiaWindow.engine.setProperty('voice', SophiaWindow.voices[audio].id)
def StartTheProgram():
    def wish():
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            a = "Good Morning. your assistance is now online and ready to assist you on your command"
            speak(a)
        elif hour >= 12 and hour < 18:
            a = "Good after noon. your assistance is now online and ready to assist you on your command"
            speak(a)
        else:
            a = "Good evening. your assistance is now online and ready to assist you on your command"
            speak(a)
    wish()
    host=config("Host")
    user=config("User")
    sql_pass=config("SqlPassword")
    while True:
        if keyboard.is_pressed('f2'):
            try:
                import pywhatkit
                sound.play()
                final=SophiaWindow.SpeechRecognition()
                if 'sophia' in final or 'sofia' in final:
                    a=final.split()
                    if a[0]=="sophia" or a[0]=="sofia":
                        final=final.replace('sophia','',1)
                        final=final.replace('sofia','',1)
                    else:
                        pass         
                if 'open' in final:
                    data=mp.connect(host = host, user = user, password = sql_pass, database="Sophia")
                    ed=data.cursor()
                    FOUND=False
                    final=final.replace('open','',1)
                    final=final.replace(' ','',1)
                    ed.execute("select name from files")
                    a=ed.fetchall()
                    filecontent=[]
                    for i in range(len(a)):
                        filecontent.append(str(a[i][0]).lower())
                    for i in filecontent:
                        if final in i:
                            ed.execute(f"select file from files where name ='{i}'")
                            location=ed.fetchall()
                            os.startfile(location[0][0])
                            FOUND=True
                            break
                    if FOUND==False:
                        ed.execute("select name from web")
                        b=ed.fetchall()
                        web=[]
                        for i in range(len(b)):
                            web.append(str(b[i][0]).lower())
                        for i in web:
                            if final in i:
                                FOUND=True
                                ed.execute(f"select web from web where name ='{i}'")
                                location=ed.fetchall()
                                webbrowser.open(location[0][0])
                                break
                        if FOUND==False:
                            win.out(f"No Keyword found name '{final}'")
                    if FOUND==True:
                        win.out(f"Opening '{final}'")
                elif "message" in final:
                    host=config("Host")
                    user=config("User")
                    sqlpassword=config("SqlPassword")
                    data=mp.connect(
                        host=host, password=sqlpassword, user=user, database="Sophia")
                    ed=data.cursor()
                    ed.execute("select Name from phone")
                    a=ed.fetchall()
                    contact_name=[]
                    for i in range(len(a)):
                        contact_name.append(str(a[i][0]).lower())
                    sp=final.split()
                    for i in contact_name:
                        if i in sp:
                            ed.execute(f"Select number from phone where name='{i}'")
                            name=i
                            break
                    no=ed.fetchall()
                    data.close()
                    if no==[]:
                        win.out("contact not found", output=False)
                    else:
                        SophiaWindow.speak("please tell the message")
                        sound.play()
                        message=SophiaWindow.SpeechRecognition(10)
                        win.out(f"sending '{message}' to '{name}'")
                        no="+91 "+str(no[0][0])
                        pywhatkit.sendwhatmsg_instantly(no,message)
                        SophiaWindow.speak("message sent!")
                elif 'play' in final or 'on youtube' in final:
                    content=final.replace('play', '', 1)   
                    content=content.replace('on youtube', '', 1)   
                    content=content.replace('search', '', 1)
                    win.out(f"Opening {content} on youtube")
                    pywhatkit.playonyt(content)

                elif 'show' in final:
                    if "contacts" in final or "numbers" in final or "contact" in final or "number" in final or "phone" in final or "phones" in final:
                        try:
                            data=mp.connect(host = host, user = user, password = sql_pass, database="Sophia")
                            ed=data.cursor()
                            ed.execute("Select name from phone")
                            names=ed.fetchall()
                            if len(names)==0:
                                win.out("Database empty for contacts")
                            else:
                                ed.execute("Select number from phone")
                                contact=ed.fetchall()
                                data.close()
                                win.out("-"*30,say=False)
                                for i in range(len(names)):
                                    win.out(f"{names[i][0]}={contact[i][0]}", say=False)
                                win.out("-"*30, say=False)
                        except Exception as err:
                            if err.__class__.__name__ == "DatabaseError":
                                win.out("unable to connect to my s q l server. please add again", output=False)
                    elif "keywords" in final or "keyword" in final or "keyboard" in final or "keyboards" in final:
                        try:
                            data=mp.connect(host = host, user = user, password = sql_pass, database="Sophia")
                            ed=data.cursor()
                            ed.execute("Select name from files")
                            filenames=ed.fetchall()
                            ed.execute("Select file from files")
                            filelocation=ed.fetchall()
                            ed.execute("Select name from web")
                            webnames=ed.fetchall()
                            ed.execute("Select web from web")
                            weblocation=ed.fetchall()
                            data.close()
                            if len(filenames)==0 and len(webnames)==0:
                                win.out("Database empty for Keywords")
                            else:
                                if len(filenames)!=0:
                                    win.out("-"*30,say=False)
                                    for i in range(len(filenames)):
                                        win.out(f"{filenames[i][0]}={filelocation[i][0]}", say=False)
                                    win.out("Keywords for System files", say=False)
                                    win.out("-"*30,say=False)
                                if len(webnames)!=0:
                                    win.out("-"*30,say=False)
                                    for i in range (len(webnames)):
                                        win.out(f"{webnames[i][0]}={weblocation[i][0]}", say=False)
                                    win.out("Keywords for URL", say=False)
                                    win.out("-"*30,say=False)
                        except Exception as err:
                            if err.__class__.__name__ == "DatabaseError":
                                win.out("unable to connect to my s q l server. please add again", output=False)
                elif "contacts" in final or "contact" in final and "save" in final or "upload" in final or "add" in final:
                    from SophiaManageDBMS import uploadContacts
                    uploadContacts()
                elif "time" in final:
                    current_time=str(datetime.datetime.now().strftime("%I:%M %p"))
                    d=f"The Current Time is {current_time}"
                    win.out(d)
                elif 'search on google' in final or 'google' in final or 'search' in final:
                    search=str(final)
                    check=search.split()
                    search=search.replace("search on google",'',1)
                    if "search" in check[0:2]:
                        search=search.replace("search",'',1)
                    search=search.replace("on google",'',1)
                    win.out(f'You asked me to search {search}')
                    pywhatkit.search(search)
                elif "weather" in final:
                    speak("please tell the city name")
                    sound.play()
                    city=SophiaWindow.SpeechRecognition()
                    w_api_key="0e1b90a815ec5b572fb4eac00e579175" #openweathermap api key
                    link=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={w_api_key}"
                    data=requests.get(link)
                    data=data.json()
                    temp=f"Weather in {city.title()}:\nTemperature={int(data['main']['temp']-273)}\N{DEGREE SIGN}C\nCondition={data['weather'][0]['main'].title()}"
                    tempsp=f"temperature in {city} is {int(data['main']['temp']-273)} degree celcius and have a {data['weather'][0]['main']} weather condition"
                    win.out(tempsp, output=False)
                    time.sleep(1)
                    win.out(temp, say=False)
                elif "type with me" in final or "tie with me" in final or "type" in final:
                    SophiaWindow.speak("ready to recognise")
                    sound.play()
                    data=SophiaWindow.SpeechRecognition(20)
                    SophiaWindow.speak("recognition completed")
                    win.out(data,say=False)                   
                elif "shutdown the pc" in final or "shutdown the computer" in final or "shutdown pc" in final or 'shutdown computer' in final or 'turn off the pc' in final or "turn off the computer" in final or 'turn off computer' in final or "turn off computer" in final:
                    SophiaWindow.speak("Turning off the pc")
                    time.sleep(1.5)
                    pywhatkit.shutdown(time=1)                
                elif "download" in final and "youtube" in final:
                    SophiaYt.yt()
                elif "change" in final and "location" in final:
                    from SophiaAddLocation import ChangeLocation
                    ChangeLocation()
                elif 'tell me about' in final or "tell me who is" in final or "tell me what is":
                    win.out('searching wikipedia', output=False)
                    final=final.replace('tell me about', '')
                    final=final.replace('tell me who is', '')
                    final=final.replace('tell me what is', '')
                    final=final.replace('what is', '')
                    final=final.replace('who is', '')
                    title=wikipedia.search(final,results=1)
                    result=wikipedia.summary(title[0], sentences=1, auto_suggest=False)
                    result=f"According to wikipedia, {result}"
                    win.out(result)
                    time.sleep(0.1)
                    SophiaWindow.speak("Should i open the wikipedia page?")
                    while True:   
                        sound.play()
                        try:
                            ans=SophiaWindow.SpeechRecognition(3)
                            if "no" in ans or "don't" in ans:
                                SophiaWindow.speak("ok, no issue")
                                break
                            elif "yes" in ans or 'sure' in ans or "open" in ans or "take" in ans or 'show' in ans:
                                win.out(f'Opening "{title[0]}" on Wikipedia')
                                webbrowser.open(f"https://en.wikipedia.org/wiki/{title[0]}")
                                break
                            else:
                                SophiaWindow.speak("sorry, can you repeat that again") 
                        except:
                            SophiaWindow.speak("please answer again")         
                else:
                    pass  
            except Exception as a:
                if (a.__class__.__name__)=="InternetException":
                    SophiaWindow.speak("Please check your internet connection")
                elif a.__class__.__name__=="KeyError":
                    SophiaWindow.speak("unable to find the location")
                    win.out(f"Unable to find the weather condition in '{city}'", say=False)

if __name__=="SophiaBackend":
    win=SophiaWindow.MainWindow()
    win.StartTheWindow("800x600+250+80", "Sophia, The Virtual Assistant", "#3AA8EC",)
    time.sleep(1.5)
    StartTheProgram()
