import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import threading
import queue

# ================== INIT ==================
speech_queue = queue.Queue()
recognizer = sr.Recognizer()

speech_lock = threading.Lock()   # 🔥 IMPORTANT FIX

news_api = "504a18e2c15b4fc594d99af4542923c0"


# ================== SPEECH THREAD ==================
def speech_worker():
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)
    engine.setProperty("volume", 1.0)

    print("Speech thread started")

    while True:
        text = speech_queue.get()
        if text is None:
            break

        # 🔥 LOCK WHILE SPEAKING
        with speech_lock:
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print("Speech error:", e)

        speech_queue.task_done()


threading.Thread(target=speech_worker, daemon=True).start()


# ================== SPEAK ==================
def speak(text):
    speech_queue.put(str(text))
    speech_queue.join()   # 🔥 wait until speaking finishes


# ================== COMMAND ==================
def processcommand(command):
    command = command.lower()

    if "alexander" in command:
        speak("As you command")
        return

    elif "open google" in command:
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    elif command.startswith("play"):
        try:
            song = command.split(" ", 1)[1]
            if song in musiclibrary.music:
                webbrowser.open(musiclibrary.music[song])
                speak(f"Now playing {song}")
            else:
                speak(f"{song} not found")
        except:
            speak("Say song name")

    # ================== NEWS ==================
    elif "news" in command:
        try:
            speak("Fetching latest news")

            response = requests.get(
                f"https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&language=en&apiKey={news_api}"
            )

            if response.status_code != 200:
                speak("Failed to fetch news")
                return

            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                speak("No news available")
                return

            # 🔥 ONE BLOCK SPEECH
            news_text = "Here are the top headlines. "

            for i, article in enumerate(articles[:5], 1):
                title = article.get("title", "No title")
                print(f"News {i}:", title)
                news_text += f"Headline {i}. {title}. "

            speak(news_text)

        except Exception as e:
            print("News error:", e)
            speak("Error getting news")

    else:
        speak("Command not recognized")


# ================== MAIN LOOP ==================
if __name__ == "__main__":

    speak("My name is Alexander, Blade of ErenGuard")

    while True:
        try:
            # 🔥 WAIT UNTIL SPEECH COMPLETELY FINISHES
            if speech_lock.locked():
                continue

            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print("You said:", command)

            if "alexander" in command.lower():
                speak("As you command")

            command = command.lower().replace("alexander", "").strip()

            if command:
                processcommand(command)

        except sr.UnknownValueError:
            print("Could not understand")

        except Exception as e:
            print("Error:", e)