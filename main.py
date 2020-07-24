'''
# List of modules that I have imported
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
from bs4 import BeautifulSoup
import requests


# Function that allows the assistant to speak
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


# Function that allows audio from the microphone to be recognised
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print(str(e))
    return said


# Function that removes the voice file from which the assistant speaks from so that it can speak again
def remove_file():
    os.remove('voice.mp3')


# Running an infinite loop in which the assistant is called when the keyword is said
global run
run = False


def calling_assistant():
    global running_main_loop
    running_main_loop = False
    while not running_main_loop:
        text = get_audio()
        if "hello" in text:
            speak("Hello, how can I help?")
            remove_file()
            running_main_loop = True
            main_loop()


def main_loop():
    running_main_loop = True
    while running_main_loop:

        text = get_audio()

        if "weather" in text:
            speak("28 degrees")
            print("28 degrees")
            remove_file()

        running_main_loop = False

    calling_assistant()


calling_assistant()
'''
