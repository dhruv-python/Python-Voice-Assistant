import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
from urllib.parse import quote_plus


# =========================================================
# VOICE ENGINE
# =========================================================

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(text):
    """Convert text into speech and also display it."""
    print("Assistant:", text)

    engine.say(text)
    engine.runAndWait()


# =========================================================
# VOICE INPUT
# =========================================================

recognizer = sr.Recognizer()


def listen():
    """Listen to the microphone and convert speech to text."""

    with sr.Microphone() as source:

        print("\nListening...")

        # Adjust microphone for background noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:
            print("No voice detected.")
            return ""

    try:
        print("Recognizing...")

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("You:", command)

        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand you. Please repeat.")
        return ""

    except sr.RequestError:
        speak("Sorry, the speech recognition service is unavailable.")
        return ""


# =========================================================
# DATE AND TIME
# =========================================================

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")

    speak(f"The current time is {current_time}")


def tell_date():
    current_date = datetime.datetime.now().strftime("%A, %d %B %Y")

    speak(f"Today is {current_date}")


# =========================================================
# WEB SEARCH
# =========================================================

def search_web(query):

    query = query.strip()

    if not query:
        speak("Please tell me what you want to search.")
        return

    speak(f"Searching for {query}")

    url = "https://www.google.com/search?q=" + quote_plus(query)

    webbrowser.open(url)


# =========================================================
# COMMAND PROCESSOR
# =========================================================

def process_command(command):

    if not command:
        return True

    # -----------------------------------------
    # HELLO
    # -----------------------------------------

    if "hello" in command or "hi" in command:

        speak("Hello! How can I help you?")

    # -----------------------------------------
    # TIME
    # -----------------------------------------

    elif "time" in command:

        tell_time()

    # -----------------------------------------
    # DATE
    # -----------------------------------------

    elif "date" in command or "today" in command:

        tell_date()

    # -----------------------------------------
    # WEB SEARCH
    # -----------------------------------------

    elif command.startswith("search for"):

        query = command.replace("search for", "", 1)

        search_web(query)

    elif command.startswith("search"):

        query = command.replace("search", "", 1)

        search_web(query)

    # -----------------------------------------
    # GOOGLE
    # -----------------------------------------

    elif "google" in command:

        speak("What should I search for?")

        query = listen()

        if query:
            search_web(query)

    # -----------------------------------------
    # EXIT
    # -----------------------------------------

    elif (
        "exit" in command
        or "quit" in command
        or "stop" in command
        or "goodbye" in command
    ):

        speak("Goodbye! Have a great day.")

        return False

    # -----------------------------------------
    # UNKNOWN COMMAND
    # -----------------------------------------

    else:

        speak(
            "I did not understand that command. "
            "You can ask me for the time, date, "
            "or a web search."
        )

    return True


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    speak(
        "Voice assistant started. "
        "You can say hello, ask for the time, "
        "ask for the date, or search the web."
    )

    running = True

    while running:

        command = listen()

        running = process_command(command)


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":
    main()