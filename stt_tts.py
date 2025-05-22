import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk


load_dotenv()


def from_mic():
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    print(speech_recognition_result.text)

from_mic()