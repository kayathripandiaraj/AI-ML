import streamlit as st
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import threading
engine=pyttsx3.init()
st.set_page_config(page_title="Voice Assistant",layout="centered")
st.title("🎤Voice Assistant")
st.markdown("Speak a command like,'What time is it','open google','What is The date','open Youtube','open Gmail' or 'What is your name'.")
def speak(text):
    def _speak():
        engine = pyttsx3.init(driverName='sapi5')  
        engine.setProperty('rate', 150)  
        engine.setProperty('volume', 1.0)  
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak).start()
def kayathri():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening......Please Speak now")
        audio=recognizer.listen(source)
        try:
            command=recognizer.recognize_google(audio)
            st.success(f'You Said:{command}')
            return command.lower()
        except sr.UnknownValueError:
            st.error("Could not understand your speech.")
            speak("sorry....I Couldn't understand.")
            return ""
        except sr.RequestError:
            st.error("Speech Recognition Service Failed.")
            speak("Sorry,The speech service is down.")
            return ""
if st.button("Start Listening"):
    command=kayathri()
    if 'time' in command:
        now=datetime.datetime.now().strftime("%H:%M:%S")
        speak(f'The time is {now}')
        st.write(f'⏱️The Current Time Is {now}')
    elif 'date' in command:
        now=datetime.datetime.now().strftime("%d/%m/%Y")
        speak(f'The Date is {now}')
        st.write(f'📅Today is {now}')
    elif 'google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")  
        st.write("🌐 Opened [Google](https://www.google.com)")
    elif 'youtube' in command:
        speak("Opening Youtube")
        webbrowser.open("https://www.youtube.com")
        st.write("📺Opening [Youtube](https://www.youtube.com)")
    elif 'gmail' in command:
        speak("opening Gmail")
        webbrowser.open("https://mail.google.com")
        st.write("📧opening [Gmail](https://mail.google.com)")
    elif 'your name' in command or 'who are you' in command:
        speak("I am Your Voice Assistant")
        st.write("🤖Iam Your Voice Assistant")
    elif command != "":
        speak("Sorry,I don't understand the command")
        st.write("Unknown Command.")

