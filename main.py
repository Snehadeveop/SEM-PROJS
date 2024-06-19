import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import subprocess

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Jarvis Sir, your personal A.I assistant. Please tell me how may I help you.")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"


# Calendar events
def add_event_to_calendar(event):
    with open("events.txt", "a") as file:
        file.write(event + "\n")
    speak("Event added to your calendar.")


def view_calendar_events():
    with open("events.txt", "r") as file:
        events = file.readlines()
    if not events:
        speak("Your calendar is empty.")
    else:
        speak("Here are your calendar events:")
        for event in events:
            print(event.strip())
            speak(event.strip())


def delete_calendar_event():
    with open("events.txt", "r") as file:
        events = file.readlines()
    if not events:
        speak("Your calendar is already empty.")
    else:
        speak("Here are your calendar events:")
        for idx, event in enumerate(events):
            speak(f"{idx + 1}. {event.strip()}")

        speak("Please enter the number of the event you want to delete:")
        event_number = int(input("Enter the event number: "))

        if event_number < 1 or event_number > len(events):
            speak("Invalid event number. Please try again.")
        else:
            event_to_delete = events.pop(event_number - 1)
            with open("events.txt", "w") as file:
                file.writelines(events)
            speak("Event deleted from your calendar.")


def edit_calendar_event():
    with open("events.txt", "r") as file:
        events = file.readlines()
    if not events:
        speak("Your calendar is empty.")
    else:
        speak("Here are your calendar events:")
        for idx, event in enumerate(events):
            speak(f"{idx + 1}. {event.strip()}")

        speak("Please enter the number of the event you want to edit:")
        event_number = int(input("Enter the event number: "))

        if event_number < 1 or event_number > len(events):
            speak("Invalid event number. Please try again.")
        else:
            speak("What would you like to change about this event?")
            speak("1. Title")
            speak("2. Start Time")
            speak("3. End Time")
            option = int(input("Enter your choice: "))
            if option == 1:
                speak("Enter the new title:")
                new_title = input("Enter the new title: ")
                events[event_number - 1] = new_title + events[event_number - 1][events[event_number - 1].find(','):]
            elif option == 2:
                speak("Enter the new start time:")
                new_start_time = input("Enter the new start time: ")
                events[event_number - 1] = events[event_number - 1][
                                           :events[event_number - 1].find(',') + 2] + new_start_time + events[
                                                                                                           event_number - 1][
                                                                                                       events[
                                                                                                           event_number - 1].find(
                                                                                                           ']'):]
            elif option == 3:
                speak("Enter the new end time:")
                new_end_time = input("Enter the new end time: ")
                events[event_number - 1] = events[event_number - 1][
                                           :events[event_number - 1].rfind(',') + 2] + new_end_time + events[
                                                                                                          event_number - 1][
                                                                                                      events[
                                                                                                          event_number - 1].find(
                                                                                                          ']'):]

            with open("events.txt", "w") as file:
                file.writelines(events)
            speak("Event details updated successfully.")

#entertaiment
def tell_joke(category=None):
    jokes = {
        'general': [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I'm reading a book on anti-gravity. It's impossible to put down!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Parallel lines have so much in common. It's a shame they'll never meet."
        ],
        'puns': [
            "What did one ocean say to the other ocean? Nothing, they just waved!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "What do you call fake spaghetti? An impasta!"
        ],
        'dad': [
            "Why did the bicycle fall over? Because it was two-tired!",
            "How does a penguin build its house? Igloos it together!",
            "I only know 25 letters of the alphabet. I don't know y.",
            "I told my wife she should embrace her mistakes. She gave me a hug."
        ]
    }

    if category:
        joke = random.choice(jokes.get(category.lower(), ["I'm sorry, I don't have jokes in that category."]))
    else:
        category, jokes_list = random.choice(list(jokes.items()))
        joke = random.choice(jokes_list)

    print(joke)
    speak(joke)


def open_entertainment():
    speak("What would you like to do for entertainment?")
    speak("You can choose from the following options:")
    speak("1. Tell me a joke")
    speak("2. Play a game")
    speak("3. Recommend movies")

    choice = takeCommand()

    if 'tell me a joke' in choice:
        tell_joke()
    elif 'play a game' in choice:
        # Execute the game script
        subprocess.Popen(["python", "game.py"])
    elif 'recommend movies' in choice:
        while True:
            speak("What genre of movies are you interested in?")
            speak("You can choose from the following options:")
            speak("1. Horror")
            speak("2. Romantic")
            speak("3. Action")
            speak("4. Sci-Fi")
            speak("5. Emotional")

            genre = takeCommand()
            if 'horror' in genre:
                speak("You might like movies such as 'The Conjuring' or 'Hereditary'.")
                break
            elif 'romantic' in genre:
                speak("You might enjoy 'The Notebook' or 'Pride and Prejudice'.")
                break
            elif 'action' in genre:
                speak("Consider watching 'The Dark Knight' or 'Mission: Impossible'.")
                break
            elif 'sci-fi' in genre:
                speak("Check out 'Inception' or 'The Matrix'.")
                break
            elif 'emotional' in genre:
                speak("You could watch 'Forrest Gump' or 'The Shawshank Redemption'.")
                break
            else:
                speak("Sorry, I couldn't understand your preference. Please try again.")


if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand()
        # Tasks execution logic
        if 'how are you' in query:
            speak("I'm doing good, thank you for asking!")
        elif 'open youtube' in query:
            speak("Opening Youtube")
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")
        elif 'open amazon' in query:
            speak("Opening Amazon")
            webbrowser.open("amazon.com")
        elif 'open my whatsapp' in query:
            speak("Opening Whatsapp")
            webbrowser.open("whatsapp.com")

            # When done using Jarvis
        elif 'thank you jarvis i\'m done' in query:
            speak("You're welcome! Goodbye Sir, have a great day!")
            break

            # Wikipedia
        elif 'open wikipedia' in query or 'search wikipedia' in query:
            speak('Searching Wikipedia...')
            try:
                if 'open wikipedia' in query:
                    query = query.replace("open wikipedia", "")
                else:
                    query = query.replace("search wikipedia", "")
                results = wikipedia.summary(query, sentences=1)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                print("An error occurred while searching Wikipedia:", e)
                speak("Sorry, I couldn't find information on that topic.")

        # For music
        elif 'jarvis play music' in query:
            music_dir = 'C:\\Users\\sneha\\PycharmProjects\\songs'
            songs = os.listdir(music_dir)
            print("Songs in the directory:", songs)
            if len(songs) == 0:
                speak("There are no songs in your music directory.")
            else:
                speak("Playing music...")
                os.startfile(os.path.join(music_dir, songs[0]))

        elif 'what is the time' in query:
            print("Query recognized for time:", query)
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f" the time is {strTime}")

        elif 'jarvis add event' in query:
            speak("What is the event title?")
            event_title = takeCommand()
            speak("When does the event start? Please provide date and time.")
            start_time = takeCommand()
            speak("When does the event end? Please provide date and time.")
            end_time = takeCommand()
            event = f"{event_title}, {start_time}, {end_time}"
            add_event_to_calendar(event)

        elif 'jarvis view calendar' in query:
            view_calendar_events()

        elif 'jarvis delete event' in query:
            delete_calendar_event()

        elif 'jarvis edit event' in query:
            edit_calendar_event()

        elif 'open entertainment' in query:
            open_entertainment()

        elif 'jarvis open vs code' in query:
            codepath = 'C:\\Users\\sneha\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
            os.startfile(codepath)
