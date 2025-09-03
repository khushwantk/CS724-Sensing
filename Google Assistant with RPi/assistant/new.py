import threading
import time
import subprocess
import subprocess
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_stop():
    print("Say stop to terminate..")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            if "stop" in command:
                print("STOP command detected. Terminating Google Assistant.")
                return True
        except sr.UnknownValueError:
            pass
        except sr.WaitTimeoutError:
            pass
    return False



def listen_for_google():
    with sr.Microphone() as source:
        # recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            if "google" in command:
                return True
        except sr.UnknownValueError:
            pass
        except sr.WaitTimeoutError:
            pass
    return False




def monitor_stop_command(assistant_process):
    while assistant_process.poll() is None:
        if listen_for_stop():
            assistant_process.terminate()
            print("Assistant terminated by 'STOP' command.")
            speak_text("Assistant stopped")
            break
        time.sleep(0.1)

# Main assistant loop
try:
    while True:
        print("Say \"Google\"....")
        if listen_for_google():
            print("Activating Assistant")
            speak_text("Activating Assistant")
            assistant_process = subprocess.Popen(["googlesamples-assistant-pushtotalk"], stdin=subprocess.PIPE)

            # Start a separate thread for listening for "STOP"
            stop_thread = threading.Thread(target=monitor_stop_command, args=(assistant_process,))
            stop_thread.start()

            assistant_process.wait()  # Wait for assistant to finish or be terminated
            stop_thread.join()  # Ensure stop_thread completes

except KeyboardInterrupt:
    print("Stopping...")
    if assistant_process and assistant_process.poll() is None:
        assistant_process.terminate()
