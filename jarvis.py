import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
import sys
import pywhatkit
import random
import wikipedia
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import threading

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
recognizer = sr.Recognizer()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()


def open_software(software_name):
    software_name = software_name.lower()
    if 'chrome' in software_name:
        speak('Opening Chrome...')
        subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
    elif 'edge' in software_name or 'microsoft edge' in software_name:
        speak('Opening Microsoft Edge...')
        subprocess.Popen([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"])
    elif 'youtube' in software_name or 'play' in software_name:
        speak('Opening YouTube...')
        pywhatkit.playonyt(software_name)
    elif 'notepad' in software_name:
        speak('Opening Notepad...')
        subprocess.Popen(['notepad.exe'])
    elif 'calculator' in software_name:
        speak('Opening Calculator...')
        subprocess.Popen(['calc.exe'])
    elif 'command prompt' in software_name or 'cmd' in software_name:
        speak('Opening Command Prompt...')
        subprocess.Popen(['cmd.exe'])
    else:
        speak(f"Sorry, I couldn't find the software {software_name

def close_software(software_name):
    software_name = software_name.lower()
    process_dict = {
        'chrome': 'chrome.exe',
        'microsoft edge': 'msedge.exe',
        'notepad': 'notepad.exe',
        'calculator': 'calculator.exe',
        'command prompt': 'cmd.exe',
    }
    for key, process in process_dict.items():
        if key in software_name:
            speak(f'Closing {key}...')
            os.system(f"taskkill /f /im {process}")
            return
    speak(f"I couldn't find any open software named {software_name}")


def search_google(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak("According to Jarvis")
        speak(result)
        return
    except Exception:
        pass
    try:
        for url in search(query, num_results=1):
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            paragraphs = soup.find_all('p')
            for para in paragraphs:
                text = para.get_text().strip()
                if len(text) > 100:
                    speak("According to Jarvis")
                    speak(text)
                    return
        speak("Sorry, I couldn't find a good answer.")
    except Exception as e:
        print("Search error:", e)
        speak("I couldn’t fetch results.")


def handle_command(text):
    if 'goodbye' in text or 'shutdown' in text:
        speak('Shutting down... Goodbye sir!')
        sys.exit()

    elif 'open' in text:
        software_name = text.replace('open', '').strip()
        open_software(software_name)

    elif 'close' in text:
        software_name = text.replace('close', '').strip()
        close_software(software_name)

    elif "what's the time" in text or "what's time now" in text or "current time" in text:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f'The time is {current_time}')

    elif 'what day is it' in text or 'what is today' in text:
        today = datetime.datetime.now().strftime('%A, %B %d')
        speak(f'Today is {today}')

    elif 'who is god' in text:
        speak('My god is Madhan, because he created me.')

    elif 'what is your name' in text or "what's your name" in text:
        speak('My name is JARVIS, your Artificial Intelligence Assistant.')

    elif 'tell me a joke' in text:
        jokes = [
            "Why did the computer go to the doctor? Because it had a virus!",
            "I told my AI friend a joke... but it didn’t get it. I guess it’s still learning!",
            "Why don’t robots ever get tired? Because they’re recharged every night!"
        ]
        speak(random.choice(jokes))

    elif 'tell me something' in text or 'fun fact' in text:
        facts = [
            "Did you know that honey never spoils?",
            "Octopuses have three hearts!",
            "The Eiffel Tower can be 15 cm taller during the summer due to heat expansion."
        ]
        speak(random.choice(facts))

    else:
        speak("Let me look that up for you.")
        search_google(text)

def listen_for_wake_word():
    with sr.Microphone() as source:
        print('Listening for wake word...')
        while True:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            recorded_audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(recorded_audio, language='en-US')
                text = text.lower()
                if 'jarvis' in text:
                    print('Wake word detected!')
                    speak('Hi Sir, how can I help you?')
                    return True
            except Exception:
                print("Could not understand audio, please try again.")
                

listener_thread = threading.Thread(target=listen_for_wake_word)
listener_thread.daemon = True
listener_thread.start()

while True:
    cmd()
