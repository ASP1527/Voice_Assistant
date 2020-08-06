
# List of modules that I have imported
import os
import playsound
import speech_recognition as sr
from gtts import gTTS
from bs4 import BeautifulSoup
import requests
from time import time, ctime
import random
import wikipedia as wiki
import config
import smtplib


global calls
calls = ["Hello, how can I help?", "What can I do for you?", "What's the time? Its time for me to help",
         "How may I help you?", "Who do you call? Me", "000110101 oops I mean what do you need help with?"]


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


'''
Functions of what it can do
'''


def get_weather_today():
    page = requests.get('https://www.bbc.co.uk/weather/2643743')
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    info = soup.find_all(class_='wr-value--temperature--c')
    # print(info)
    high_today = info[0].get_text()
    low_today = info[1].get_text()
    print(high_today)
    print(low_today)
    tie = time()
    timeData = ctime(tie)
    splitData = timeData.split(" ")
    times = splitData[4]
    times = times.split(":")
    hour = times[0]
    hour = int(hour)
    if hour > 17 or hour < 5:
        speak("Right now, it is " + high_today)
        remove_file()
    else:
        speak("Today, right now, it is " +
              high_today + ". Today there is a low of " + low_today)
        remove_file()


def get_news():
    page = requests.get('https://www.bbc.co.uk/news')
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    mainHeadline = soup.find(
        class_='gs-c-promo-heading__title gel-paragon-bold nw-o-link-split__text')

    headline1 = mainHeadline.get_text()

    secondaryHeadlines = soup.find_all(
        class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text')

    headline2 = secondaryHeadlines[0].get_text()

    headline3 = secondaryHeadlines[1].get_text()

    speak("Here are the top 3 headlines for today on BBC News")
    remove_file()
    speak(headline1)
    remove_file()
    speak(headline2)
    remove_file()
    speak(headline3)
    remove_file()


def get_time():
    tie = time()
    timeData = ctime(tie)
    splitData = timeData.split(" ")
    times = splitData[4]
    times = times.split(":")
    hour = times[0]
    minutes = times[1]
    speak("It's " + hour + " " + minutes)
    remove_file()


def wiki_search():
    try:
        speak("What would you like to search for?")
        remove_file()
        toFind = get_audio()
        #toFind = "python"
        info = wiki.summary(toFind, sentences=2)
        speak(info)
        remove_file()
    except:
        speak("An error has occured, please try again later.")
        remove_file()


def send_email():
    try:
        emailAddress = "pythonautomator1@gmail.com"
        emailPassword = ""
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(emailAddress, emailPassword)
        speak("What's the subject?")
        remove_file()
        subject = get_audio()
        #subject = "tester"
        speak("What's the message?")
        remove_file()
        msg = get_audio()
        #msg = "something"
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(emailAddress, config.email_address, message)
        server.quit()
        speak("The email has been sent.")
        remove_file()
    except:
        speak("An error has occured, please try again later.")
        remove_file()


'''
end of functions
'''


# Running an infinite loop in which the assistant is called when the keyword is said
global run
run = False


def calling_assistant():
    global running_main_loop
    running_main_loop = False
    randomCall = random.randint(0, len(calls)-1)
    randomC = calls[randomCall]
    while not running_main_loop:
        text = get_audio()
        #text = "friday"
        if "friday" in text or "Friday" in text:
            speak(randomC)
            remove_file()
            running_main_loop = True
            main_loop()


def main_loop():
    running_main_loop = True
    while running_main_loop:

        text = get_audio()
        #text = "search"

        if "weather" in text:
            get_weather_today()
        elif "news" in text:
            get_news()
        elif "time" in text:
            get_time()
        elif "search" in text:
            wiki_search()
        elif "send" in text and "email" in text:
            send_email()
        else:
            speak("I am not sure how to do that at the moment")
            remove_file()

        running_main_loop = False

    calling_assistant()


calling_assistant()
