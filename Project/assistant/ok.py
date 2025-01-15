import struct
import pyaudio
import pvporcupine
import pyttsx3

import subprocess
import speech_recognition as sr
import threading
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak_text(text):
    engine.say(text)
    engine.runAndWait()



def listen_for_stop():
    print("Say stop")
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
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            if "google" in command:
                print("STOP command detected. Terminating Google Assistant.")
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


try:
    porcupine = pvporcupine.create(
        access_key='Fbe/07GuTo/vPbup1myDUf0om3TN3zb7/kH6jYlkskKQpCjUDdVmjg==',
        keywords=['picovoice'],
        # keyword_paths=['ogl.ppn'],
        )
    paud=pyaudio.PyAudio()
    audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
    while True:
        print("Say \"Picovoice\"....")
        keyword=audio_stream.read(porcupine.frame_length)
        keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)
        keyword_index=porcupine.process(keyword)
        if keyword_index>=0:
            speak_text("Activating Assistant")

            assistant_process = subprocess.Popen(["googlesamples-assistant-pushtotalk"],stdin=subprocess.PIPE)

            # Listen for "STOP" while Assistant is active

            # while assistant_process.poll() is None:
            #     print("Say 'STOP' to terminate the Assistant...")
            #     if listen_for_stop():
            #         assistant_process.terminate()
            #         print("Assistant terminated by 'STOP' command.")
            #         speak_text("Assistant stopped")
            #         break  # Exit the loop to stop further detection

            # assistant_process.wait()

            stop_thread = threading.Thread(target=monitor_stop_command, args=(assistant_process,))
            stop_thread.start()

            # assistant_process.wait()  # Wait for assistant to finish or be terminated
            stop_thread.join()  # Ensure stop_thread completes



except KeyboardInterrupt:
    print("Stopping...")
    if assistant_process and assistant_process.poll() is None:
        assistant_process.terminate()

# finally:
#     if porcupine is not None:
#         porcupine.delete()
#     if audio_stream is not None:
#         audio_stream.close()
#     if paud is not None:
#         paud.terminate()




# export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
