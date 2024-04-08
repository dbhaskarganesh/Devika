import speech_recognition as sr
import spacy
from spacy.matcher import PhraseMatcher
import threading
import time
import webbrowser
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Attempt to load English model for spaCy
try:
    nlp = spacy.load("en_core_web_sm")
except:
    speak("Error loading spaCy model. Make sure you have 'en_core_web_sm' installed.")
    print("Error loading spaCy model. Make sure you have 'en_core_web_sm' installed.")
    exit()

# Initialize PhraseMatcher
matcher = PhraseMatcher(nlp.vocab)

# Extend the list of commands for the assistant
commands = [
    "what's the weather like",
    "tell me a joke",
    "open Google",
    "open Gmail",
    "play music",
    "set a timer",
    "send an email",
    "search for news"
]

# Add commands to PhraseMatcher
patterns = [nlp(text) for text in commands]
matcher.add("Commands", None, *patterns)

# Function to simulate action of sending an email
def send_email():
    speak("Sending an email...")
    print("Sending an email...")
    # Here you would add the code to integrate with an email service

# Function to handle user commands with added functionalities
def handle_command(command):
    if "weather" in command:
        speak("The weather is sunny today.")
    elif "joke" in command:
        joke = "Why don't scientists trust atoms? Because they make up everything!"
        speak(joke)
    elif "Google" in command:
        speak("Opening Google...")
        webbrowser.open('http://www.google.com')
    elif "Gmail" in command:
        speak("Opening Gmail...")
        webbrowser.open('http://www.gmail.com')
    elif "music" in command:
        speak("Playing music...")
        # Add code to play music
    elif "timer" in command:
        speak("Setting a timer for 10 seconds...")
        time.sleep(10)
        speak("Timer done!")
    elif "email" in command:
        send_email()
    elif "news" in command:
        speak("Searching for the latest news...")
        webbrowser.open('https://news.google.com')
        search_for_news()



def search_for_news():
    # Placeholder for searching news
    speak("Here are the latest news headlines...")
    print("Searching for the latest news...")

# Function to process user speech with added error handling
def process_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        speak("Recognizing...")
        text = recognizer.recognize_google(audio)
        doc = nlp(text)
        matches = matcher(doc)
        for match_id, start, end in matches:
            command = doc[start:end].text
            handle_command(command)
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that.")
    except sr.RequestError as e:
        speak(f"Could not request results from Google Speech Recognition service; {e}")

# Main loop to keep the assistant listening; consider threading for production use
try:
    while True:
        process_speech()
except KeyboardInterrupt:
    speak("Voice assistant terminated.")
    print("Voice assistant terminated.")
