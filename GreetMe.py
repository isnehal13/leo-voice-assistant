import pyttsx3
import datetime

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    hour  = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning,ma'am")
    elif hour >12 and hour<=18:
        speak("Good Afternoon, ma'am")

    else:
        speak("Good Evening, ma'am")

    speak("Please tell me, How can I help you ?")
