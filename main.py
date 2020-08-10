
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
import smtplib
import tkinter as tk
from tkinter import filedialog, Text
import os
import config


transcribe = []


configured = False

if os.path.isfile('config.py'):
    configured = True

if configured == False:
    root = tk.Tk()
    items = []
    root.title('Configuring')

    canvas = tk.Canvas(root, height=700, width=800, bg="#008080")
    canvas.pack()

    frame = tk.Frame(root, bg="white")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def addToFile():
        item = e.get()
        item = str(item)
        items.append(item)
        for widget in frame.winfo_children():
            widget.destroy()
        for i in range(0, len(items)):
            label = tk.Label(frame, text=items[i], bg="#C0C0C0")
            label.pack()
        if len(items) > 2:
            root.destroy()

    label = tk.Label(
        text="Enter 3 Email Addresses that you would like to send emails to using this voice assistant:")
    label.pack()

    e = tk.Entry(root, width=50)
    e.pack()

    add = tk.Button(root, text="Click", padx=10, pady=5, fg="white",
                    bg="#C0C0C0", font=('helvetica', 9), command=addToFile)
    add.pack()

    root.mainloop()

    with open('config.py', 'w') as f:
        f.write("email_address = ")
        f.write('"')
        f.write(items[0])
        f.write('"')
        f.write("\n")
        f.write("email_address2 = ")
        f.write('"')
        f.write(items[1])
        f.write('"')
        f.write("\n")
        f.write("email_address3 = ")
        f.write('"')
        f.write(items[2])
        f.write('"')


global calls
calls = ["Hello, how can I help?", "What can I do for you?", "What's the time? Its time for me to help",
         "How may I help you?", "Who do you call? Me", "000110101 oops I mean what do you need help with?"]


# Function that allows the assistant to speak
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    f = open('transcript.txt', 'a')
    f.write(text)
    f.write('\n')


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
    times = splitData[3]
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
    times = splitData[3]
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
        emailPassword = "Python1234"
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


def get_date():
    tie = time()
    timeData = ctime(tie)
    splitData = timeData.split(" ")
    day = splitData[0]
    month = splitData[1]
    date1 = splitData[3]
    date = (day + " " + month + " " + date1)
    speak(date)
    remove_file()


def reset_email_addresses():
    os.remove('config.py')
    speak("I have removed the email addresses, please restart the program to reset them.")
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
        #text = get_audio()
        text = "hello"
        if "hello" in text or "Friday" in text:
            speak(randomC)
            remove_file()
            running_main_loop = True
            main_loop()


def main_loop():
    running_main_loop = True
    while running_main_loop:

        #text = get_audio()
        text = "time"

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
        elif "date" in text or "day" in text or "month" in text:
            get_date()
        elif ("reset" in text or "remove" in text) and ("email" in text or "emails" in text):
            reset_email_addresses()
        else:
            speak("I am not sure how to do that at the moment")
            remove_file()

        running_main_loop = False

    calling_assistant()


calling_assistant()
