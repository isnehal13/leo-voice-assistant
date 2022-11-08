
import datetime,wikipedia,webbrowser,os,random,requests,pyautogui,playsound,subprocess,time
import urllib.request,bs4 as bs,sys,threading
 
import Annex, wolframalpha
from ttkthemes import themed_tk
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk,Image
import sqlite3,pyjokes,pywhatkit,random
from functools import partial
import getpass
import pyttsx3
import PIL

from GreetMe import greetMe
 
 
 
try:
    app=wolframalpha.Client("WWYUV5-AUEX2J7R67")  #API key for wolframalpha
except Exception as e:
    pass
 
#setting chrome path
chrome_path="C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
 
def there_exists(terms,query):
    for term in terms:
        if term in query:
            return True
 
def CommandsList():
    '''show the command to which voice assistant is registered with'''
    os.startfile('Commands List.txt')
 
def clearScreen():
    ''' clear the scrollable text box'''
    SR.scrollable_text_clearing()
 
def greet():
    conn = sqlite3.connect('GreetMe')
    mycursor=conn.cursor()
    hour=int(datetime.datetime.now().hour)
    if hour>=4 and hour<12:
        mycursor.execute('select sentences from goodmorning')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    elif hour>=12 and hour<18:
        mycursor.execute('select sentences from goodafternoon')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    elif hour>=18 and hour<21:
        mycursor.execute('select sentences from goodevening')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    else:
        mycursor.execute('select sentences from night')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    conn.commit()
    conn.close()
    SR.speak("\nMyself leo. How may I help you?")
 
def mainframe():
    """Logic for execution task based on query"""
    SR.scrollable_text_clearing()
    greetMe()
    query_for_future=None
    try:
        while(True):
            query=SR.takeCommand().lower()          #converted the command in lower case of ease of matching
 
            #wikipedia search
            if there_exists(['search wikipedia for','from wikipedia'],query):
                SR.speak("Searching wikipedia...")
                if 'search wikipedia for' in query:
                    query=query.replace('search wikipedia for','')
                    results=wikipedia.summary(query,sentences=2)
                    SR.speak("According to wikipedia:\n")
                    SR.speak(results)
                elif 'from wikipedia' in query:
                    query=query.replace('from wikipedia','')
                    results=wikipedia.summary(query,sentences=2)
                    SR.speak("According to wikipedia:\n")
                    SR.speak(results)
            elif there_exists(['wikipedia'],query):
                SR.speak("Searching wikipedia....")
                query=query.replace("wikipedia","")
                results=wikipedia.summary(query,sentences=2)
                SR.speak("According to wikipedia:\n")
                SR.speak(results)
 
            #jokes
            elif there_exists(['tell me joke','tell me a joke','tell me some jokes','i would like to hear some jokes',"i'd like to hear some jokes",
                            'can you please tell me some jokes','i want to hear a joke','i want to hear some jokes','please tell me some jokes',
                            'would like to hear some jokes','tell me more jokes'],query):
                SR.speak(pyjokes.get_joke(language="en", category="all"))
                query_for_future=query
            elif there_exists(['one more','one more please','tell me more','i would like to hear more of them','once more','once again','more','again'],query) and (query_for_future is not None):
                SR.speak(pyjokes.get_joke(language="en", category="all"))
 
            #asking for name
            elif there_exists(["what is your name","what's your name","tell me your name",'who are you'],query):
                SR.speak("My name is leo and I'm here to serve you.")
            #How are you
            elif there_exists(['how are you'],query):
                conn = sqlite3.connect('leo.db')
                mycursor=conn.cursor()
                mycursor.execute('select sentences from howareyou')
                result=mycursor.fetchall()
                temporary_data=random.choice(result)[0]
                SR.updating_ST_No_newline(temporary_data+'😃\n')
                SR.nonPrintSpeak(temporary_data)
                conn.close()
            #what is my name
            elif there_exists(['what is my name','tell me my name',"i don't remember my name"],query):
                SR.speak("Your name is "+str(getpass.getuser()))
 
           
            #google, youtube and location
            #playing on youtube
            elif there_exists(['open youtube and play','on youtube'],query):
                if 'on youtube' in query:
                    SR.speak("Opening youtube")
                    pywhatkit.playonyt(query.replace('on youtube',''))
                else:
                    SR.speak("Opening youtube")
                    pywhatkit.playonyt(query.replace('open youtube and play ',''))
                break
            elif there_exists(['play some songs on youtube','i would like to listen some music','i would like to listen some songs','play songs on youtube'],query):
                SR.speak("Opening youtube")
                pywhatkit.playonyt('play random songs')
                break
            elif there_exists(['open youtube','access youtube'],query):
                SR.speak("Opening youtube")
                webbrowser.get(chrome_path).open("https://www.youtube.com")
                break
            elif there_exists(['open google and search','google and search'],query):
                url='https://google.com/search?q='+query[query.find('for')+4:]
                webbrowser.get(chrome_path).open(url)
                break
            #image search
            elif there_exists(['show me images of','images of','display images'],query):
                url="https://www.google.com/search?tbm=isch&q="+query[query.find('of')+3:]
                webbrowser.get(chrome_path).open(url)
                break
            elif there_exists(['search for','do a little searching for','show me results for','show me result for','start searching for'],query):
                SR.speak("Searching.....")
                if 'search for' in query:
                    SR.speak(f"Showing results for {query.replace('search for','')}")
                    pywhatkit.search(query.replace('search for',''))
                elif 'do a little searching for' in query:
                    SR.speak(f"Showing results for {query.replace('do a little searching for','')}")
                    pywhatkit.search(query.replace('do a little searching for',''))
                elif 'show me results for' in query:
                    SR.speak(f"Showing results for {query.replace('show me results for','')}")
                    pywhatkit(query.replace('show me results for',''))
                elif 'start searching for' in query:
                    SR.speak(f"Showing results for {query.replace('start searching for','')}")
                    pywhatkit(query.replace('start searching for',''))
                break
 
            elif there_exists(['open google'],query):
                SR.speak("Opening google")
                webbrowser.get(chrome_path).open("https://www.google.com")
                break
            elif there_exists(['find location of','show location of','find location for','show location for'],query):
                if 'of' in query:
                    url='https://google.nl/maps/place/'+query[query.find('of')+3:]+'/&amp'
                    webbrowser.get(chrome_path).open(url)
                    break
                elif 'for' in query:
                    url='https://google.nl/maps/place/'+query[query.find('for')+4:]+'/&amp'
                    webbrowser.get(chrome_path).open(url)
                    break
            elif there_exists(["what is my exact location","What is my location","my current location","exact current location"],query):
                url = "https://www.google.com/maps/search/Where+am+I+?/"
                webbrowser.get().open(url)
                SR.speak("Showing your current location on google maps...")
                break
            elif there_exists(["where am i"],query):
                Ip_info = requests.get('https://api.ipdata.co?api-key=test').json()
                loc = Ip_info['region']
                SR.speak(f"You must be somewhere in {loc}")
 
            #who is searcing mode
            elif there_exists(['who is','who the heck is','who the hell is','who is this'],query):
                query=query.replace("wikipedia","")
                results=wikipedia.summary(query,sentences=1)
                SR.speak("According to wikipdedia:  ")
                SR.speak(results)
 
            
             # top 5 news
            elif there_exists(['top 5 news','top five news','listen some news','news of today'],query):
                news=Annex.News(scrolledtext)
                news.show()
                
                
            
            
            
            #whatsapp message
            elif there_exists(['whatsapp','send a whatsapp message','send whatsapp message','please send a whatsapp message'],query):
                whatsapp=Annex.WhatsApp(scrollable_text)
                whatsapp.send()
                del whatsapp
           
            
           
 
            #time and date
            elif there_exists(['the time'],query):
                strTime =datetime.datetime.now().strftime("%H:%M:%S")
                SR.speak(f"Sir, the time is {strTime}")
            elif there_exists(['the date'],query):
                strDay=datetime.date.today().strftime("%B %d, %Y")
                SR.speak(f"Today is {strDay}")
            elif there_exists(['what day it is','what day is today','which day is today',"today's day name please"],query):
                SR.speak(f"Today is {datetime.datetime.now().strftime('%A')}")
 
           
 
 
           
            #shutting down system
            elif there_exists(['exit','quit','shutdown','shut up','goodbye','shut down'],query):
                SR.speak("shutting down")
                sys.exit()
 
            elif there_exists(['none'],query):
                pass
            elif there_exists(['stop the flow','stop the execution','halt','halt the process','stop the process','stop listening','stop the listening'],query):
                SR.speak("Listening halted.")
                break
            #it will give online results for the query
            elif there_exists(['search something for me','to do a little search','search mode','i want to search something'],query):
                SR.speak('What you want me to search for?')
                query=SR.takeCommand()
                SR.speak(f"Showing results for {query}")
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Sorry, but there is a little problem while fetching the result.")
 
            #what is the capital
            elif there_exists(['what is the capital of','capital of','capital city of'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Sorry, but there is a little problem while fetching the result.")
 
            elif there_exists(['temperature'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Internet Connection Error")
            elif there_exists(['+','-','*','x','/','plus','add','minus','subtract','divide','multiply','divided','multiplied'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Internet Connection Error")
 
            else:
                SR.speak("Sorry it did not match with any commands that i'm registered with. Please say it again.")
    except Exception as e:
        pass
 
def gen(n):
    for i in range(n):
        yield i
 
class MainframeThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        mainframe()
 
def Launching_thread():
    Thread_ID=gen(1000)
    global MainframeThread_object
    MainframeThread_object=MainframeThread(Thread_ID.__next__(),"Mainframe")
    MainframeThread_object.start()
 
if __name__=="__main__":
        #tkinter code
        root=themed_tk.ThemedTk()
        root.set_theme("winnative")
        root.geometry("{}x{}+{}+{}".format(745,360,int(root.winfo_screenwidth()/2 - 745/2),int(root.winfo_screenheight()/2 - 360/2)))
        root.resizable(0,0)
        root.title("leo")
        root.iconbitmap('C:/Users/Snehal/Downloads/you.ico')
        root.configure(bg='#5F2D61')
        scrollable_text=scrolledtext.ScrolledText(root,state='disabled',height=15,width=87,relief='sunken',bd=5,wrap=tk.WORD,bg='#add8e6',fg='#800000')
        scrollable_text.place(x=10,y=10)
        mic_img=Image.open("D:/jarvis1/Mic2.jpg")
        mic_img=mic_img.resize((55,55),Image.ANTIALIAS)
        mic_img=ImageTk.PhotoImage(mic_img)
        Speak_label=tk.Label(root,text="SPEAK:",fg="#FFD700",font='"Times New Roman" 12 ',borderwidth=0,bg='#2c4557')
        Speak_label.place(x=250,y=300)
        """Setting up objects"""
        SR=Annex.SpeakRecog(scrollable_text)    #Speak and Recognition class instance
        Listen_Button=tk.Button(root,image=mic_img,borderwidth=0,activebackground='#2c4557',bg='#2c4557',command=Launching_thread)
        Listen_Button.place(x=330,y=280)
        myMenu=tk.Menu(root)
        m1=tk.Menu(myMenu,tearoff=0) #tearoff=0 means the submenu can't be teared of from the window
        m1.add_command(label='Commands List',command=CommandsList)
        myMenu.add_cascade(label="Help",menu=m1)
        myMenu.add_cascade(label="Clear Screen",command=clearScreen)
        root.config(menu=myMenu)
        root.mainloop()
