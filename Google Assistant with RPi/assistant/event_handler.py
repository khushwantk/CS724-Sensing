from platypush.context import get_bus
from platypush.message.event.assistant import SpeechRecognizedEvent

# Define a function to handle recognized speech events
def on_speech_recognized(event):
    text = event.phrase
    print(f"Recognized speech: {text}")

    # Add conditional logic based on recognized phrases
    if "weather" in text.lower():
        print("Triggering weather action.")
        # Perform an action, e.g., fetch weather info
    elif "news" in text.lower():
        print("Triggering news action.")
        # Perform an action, e.g., fetch news info

# Register the event handler
bus = get_bus()
bus.register_handler(SpeechRecognizedEvent, on_speech_recognized)

# Keep the script running to listen for events
try:
    while True:
        pass
except KeyboardInterrupt:
    pass
