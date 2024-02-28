import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import subprocess 
import openai
import os
import time
import pyperclip
import pyautogui
from selenium import webdriver
import sys

def print_with_delay(text, delay=0.007):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Print a newline at the end

listener = sr.Recognizer()

# Adjust the recognizer's energy threshold
listener.energy_threshold = 300  # Adjust this value as needed

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

print_with_delay('Hello! I am Jarvis. Your personal assistant.')
#talk('Hello! I am Jarvis. Your personal assistant.')
print_with_delay('How can I help you?')
#talk('How can I help you?')

openai.api_key = ''
def take_command():
    try:
        with sr.Microphone(sample_rate=48000, chunk_size=2048) as source:
            print_with_delay('I am listening....')
            talk('Sir')
            listener.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            
            if 'jarvis' not in command:
                command = None  # Ignore commands without "jarvis"
            else:
                command = command.replace('jarvis', '').strip()
            
    except Exception as e:
        print_with_delay(f"Error in voice recognition: {e}")
        command = None

    return command
def append_to_notepad(text):
    try:
        with open('output.txt', 'a') as file:
            for char in text:
                file.write(char)
                file.flush()
                time.sleep(0.007)  # Delay of 7 milliseconds
            file.write('\n\n')  # Add separation for multiple inputs

        subprocess.Popen(['notepad.exe', 'output.txt'])

    except Exception as e:
        print_with_delay(f"Error appending to notepad: {e}")
def get_current_url():
    try:
        pyautogui.hotkey('ctrl', 'l')  # Selects the URL bar
        pyautogui.hotkey('ctrl', 'c')  # Copies the URL
        time.sleep(1)  # Wait briefly to allow the copy action
        return pyperclip.paste()
    except Exception as e:
        print_with_delay(f"Error retrieving URL: {e}")
        return None
def download_video():
    youtube_url = get_current_url()

    if youtube_url:
        # Modify the URL to fit the format expected by the new website
        modified_url = f"https://ytmp3.cc/{youtube_url}"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(modified_url)

    else:
        talk("Sorry, I couldn't retrieve the YouTube URL. Please ensure a browser tab is active.")



def enable():
    os.system("netsh interface set interface 'Wi-Fi' enabled")

def disable():
    os.system("netsh interface set interface 'Wi-Fi' disabled")

def run_jarvis():
    command = take_command()
    
    if command is None:
        return  # Ignore commands without "jarvis"

    print_with_delay('User:' + command)

    # The rest of your code for processing the command...

    if 'download this video' in command:
        talk('Sure, let me download this video for you.')
        download_video()

    elif 'write' in command:
        talk('Sure, let me write that for you.')
    
        prompt = f"Write this: {command.replace('write', '').strip()}"

        try:
            response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
            )

            if 'choices' in response:
                generated_text = response['choices'][0]['text']
                print_with_delay('ChatGPT: ' + generated_text)
                time.sleep(5)
                append_to_notepad(generated_text)
                talk('I have written that for you.')

        except Exception as e:
            print_with_delay(f"Error connecting to OpenAI: {e}")


    elif 'play' in command:
        print_with_delay('Analysing...')
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        print_with_delay('The current time is ' + current_time)
        talk('The current time is ' + current_time)
    elif 'wiki' in command:
        query = command.split('wiki')[-1].strip()
        talk('Searching for ' + query)
        try:
            info = wikipedia.summary(query, 1)
            print_with_delay(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options
            talk(f"Which {query} are you referring to? I found multiple options. Try specifying more.")
            print_with_delay("Disambiguation Error - Multiple options found:", options)
        except wikipedia.exceptions.PageError as e:
            talk(f"Sorry, I couldn't find information about {query}. Please try again.")
            print_with_delay("Page Error - No page found for:", query)

    elif 'turn on wi-fi' in command:
        print_with_delay('Turning on Wi-Fi')
        talk('Turning on Wi-Fi')
        enable()
    elif 'turn off wi-fi' in command:
        print_with_delay('Turning off Wi-Fi')
        talk('Turning off Wi-Fi')
        disable()
    elif 'open' in command:
        app = command.replace('open', '').strip()
        
        if 'chrome' in app:
                subprocess.Popen(['C:/Program Files/Google/Chrome/Application/Chrome.exe'])
                print_with_delay(f"Opening {app}")
                talk(f"Opening {app}")
        elif 'notepad' in app:
                subprocess.Popen(['notepad.exe'])
                print_with_delay(f"Opening {app}")
                talk(f"Opening {app}")  
        elif 'nearby share' in app:
                subprocess.Popen(['C:/Program Files/Google/NearbyShare/nearby_share.exe'])
                print_with_delay(f"Opening {app}")
                talk(f"Opening {app}")  
    elif 'open ai' in command:
            talk('Sure, let me connect to OpenAI.')

            prompt = f"Your command: {command}. Your role: You are a personal assistant like Jarvis from the Iron Man movie."
            # Add the user's command to the prompt for OpenAI to understand the context

            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=100
                )

                if 'choices' in response:
                    generated_text = response['choices'][0]['text']
                    print_with_delay('ChatGPT: ' + generated_text)
                    talk(generated_text)

            except Exception as e:
                print_with_delay(f"Error connecting to OpenAI: {e}")
    elif 'search' in command:
        query = command.replace('search', '').strip()
        talk('Searching Google for ' + query)
        
        try:
            pywhatkit.search(query)
        except Exception as e:
            print_with_delay(f"Error during Google search: {e}")
            talk("Sorry, I couldn't perform the search. Please try again.")


        # For any other unmatched command, send it to OpenAI
    else:
            #talk("I'm not sure what you're asking. Let me try to understand.")

            prompt = f"Your command: {command}. Your role: You are a personal assistant like Jarvis from the Iron Man movie."

            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=100
                )

                if 'choices' in response:
                    generated_text = response['choices'][0]['text']
                    print_with_delay('ChatGPT: ' + generated_text)
                    talk(generated_text)

            except Exception as e:
                print_with_delay(f"Error connecting to OpenAI: {e}")    

def main():
    while True:
        run_jarvis()

if __name__ == "__main__":
    main()