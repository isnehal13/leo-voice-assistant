import audioop
import datetime,subprocess,os,pyautogui,string,random,time
import pyttsx3
import speech_recognition as sr
import sounddevice,pywhatkit
from scipy.io.wavfile import write
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import pyperclip,cv2,playsound,requests,json 
from ttkthemes import themed_tk as tkth
import tkinter.scrolledtext as scrolledtext
from functools import partial
import tkinter.messagebox as tmsg,sqlite3

class SpeakRecog:
    def __init__(self,scrollable_text):
        self.scrollable_text=scrollable_text
    #database connection
    conn = sqlite3.connect('leo.db')
    mycursor=conn.cursor()

    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    
    conn.commit()
    conn.close()
    scrollable_text=None
    def STS(self,scrollable_text):
        '''This is scrollable text setter '''
        self.scrollable_text=scrollable_text
    def updating_ST(self,data):
        self.scrollable_text.configure(state='normal')
        self.scrollable_text.insert('end',data+'\n')
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.see('end')
        self.scrollable_text.update()
    def updating_ST_No_newline(self,data):
        self.scrollable_text.configure(state='normal')
        self.scrollable_text.insert('end',data)
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.see('end')
        self.scrollable_text.update()
    def scrollable_text_clearing(self):
        self.scrollable_text.configure(state='normal')
        self.scrollable_text.delete(1.0,'end')
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.update()
    def speak(self,audio):
        """It speaks the audio"""
        self.updating_ST(audio)
        self.engine.say(audio)
        # engine.save_to_file('Hello World', 'test.mp3')
        self.engine.runAndWait()
        # engine.stop()

    def nonPrintSpeak(self,audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def takeCommand(self):
        """It take microphone input from the user and return string"""
        recog=sr.Recognizer()
        #mic=sr.Microphone()
        r = sr.Recognizer()
        with sr.Microphone() as source:
           # r.adjust_for_ambient_noise(source)
            self.updating_ST("\nListening...")
            recog.pause_threshold = 1
           # r.energy_threshold = 45.131829621150224
            #print(sr.Microphone.list_microphone_names())
            #print(r.energy_threshold)
            audio=recog.listen(source)
        try:
            self.updating_ST("Recognizing...")
            query= recog.recognize_google(audio)
            self.updating_ST(f"You: {query}\n")
        except Exception as e:
            # print(e)
            self.updating_ST("Say that again please...")
            return 'None'
        return query



class TextSpeech:
    def txtspk(self):
        SR=SpeakRecog(None)
        SR.nonPrintSpeak(self.text.get(1.0,tk.END))
        del SR
    

    def __init__(self):
        self.root=tkth.ThemedTk()
        self.root.get_themes()
        self.root.set_theme("radiance")
        self.root.resizable(0,0)
        self.root.configure(background='black')
        self.root.title("Text to Speech")
        self.root.iconbitmap('C:/Users/SnehalDownloads/ttsp1.ico')
        #root widget
        self.text=scrolledtext.ScrolledText(self.root,width=30,height=10,wrap=tk.WORD,padx=10,pady=10,borderwidth=5,relief=tk.RIDGE)
        self.text.grid(row=0,columnspan=3)
        #buttons
        self.listen_btn=ttk.Button(self.root,text="Listen",width=7,command=self.txtspk).grid(row=2,column=0,ipadx=2)
        self.clear_btn=ttk.Button(self.root,text="Clear",width=7,command=lambda:self.text.delete(1.0,tk.END)).grid(row=2,column=1,ipadx=2)
        self.open_btn=ttk.Button(self.root,text="Open",width=7,command=self.opentxt).grid(row=2,column=2,ipadx=2)
        self.root.focus_set()
        self.root.mainloop()

class note:
    def Note(self,data):
        date=datetime.datetime.now()
        filename=str(date).replace(':','-')+'-note.txt'
        a=os.getcwd()
        if not os.path.exists('Notes'):
            os.mkdir('Notes')
        os.chdir(a+r'\Notes')
        with open(filename,'w') as f:
            f.write(data)
        subprocess.open(['notepad.exe',filename])
        os.chdir(a)

class screenshot:
    def takeSS(self):
        img_captured=pyautogui.screenshot()
        a=os.getcwd()
        if not os.path.exists("Screenshots"):
            os.mkdir("Screenshots")
        os.chdir(a+'\Screenshots')
        ImageName='screenshot-'+str(datetime.datetime.now()).replace(':','-')+'.png'
        img_captured.save(ImageName)
        os.startfile(ImageName)
        os.chdir(a)




class News:
    def __init__(self,scrollable_text):
        self.SR=SpeakRecog(scrollable_text)
    def show(self):
        self.SR.speak("Showing top 5 news of today.")
        self.SR.scrollable_text_clearing()
        self.SR.updating_ST("-----------------------------Top 5 news of all categories.----------------------------")
        r=requests.get('http://newsapi.org/v2/top-headlines?country=in&apiKey=064affb984394084bb7339495e2218d9')
        data=json.loads(r.content)
        for i in range(5):
            self.SR.updating_ST_No_newline(f'News {i+1}:  ')
            self.SR.speak(data['articles'][i]['title']+'\n')



class WhatsApp:
    def __init__(self,scrollable_text):
            self.SR=SpeakRecog(scrollable_text)
    def send(self):
            self.SR.speak("Please tell me the mobile number whom do you want to send message.")
            mobile_number=None
            while(True):
                mobile_number=self.SR.takeCommand().replace(' ','')
                if mobile_number[0]=='0':
                    mobile_number=mobile_number[1:]
                if not mobile_number.isdigit() or len(mobile_number)!=10:
                    self.SR.speak("Please say it again")
                else:
                    break
            mobile_number.replace(' 8108283710','8291020427')
            self.SR.speak("Tell me your message......")
            message=self.SR.takeCommand()
            self.SR.speak("Opening whatsapp web to send your message.")
            self.SR.speak("Please be patient, sometimes it takes time.\nOR In some cases it does not works.")
            while(True):
                try:
                    pywhatkit.sendwhatmsg("+91"+8108283710,message,datetime.datetime.now().hour,datetime.datetime.now().minute+1)
                    break
                except Exception:
                    pass
            time.sleep(20)
            self.SR.speak('Message sent succesfully.')


class Weather:
    def show(self,scrollable_text):
        SR=SpeakRecog(scrollable_text)
        base_url = ""
        data=requests.get(base_url).json()
        SR.scrollable_text_clearing()
        SR.speak("-----------------------------Weather Report of mumbai City------------------------------")
        SR.updating_ST("Temperature:   "+str(int(data['main']['temp']))+' Celsius\n'+
                        "Wind Speed:    "+str(data['wind']['speed'])+' m/s\n'+
                        "Latitude:      "+str(data['coord']['lat'])+
                        "\nLongitude:     "+str(data['coord']['lon'])+
                        "\nDescription:   "+str(data['weather'][0]['description'])+'\n')