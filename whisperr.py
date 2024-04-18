import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
import keyboard
import openai
from pathlib import Path
import sys
import subprocess
import os
from langid import classify as langid_classify
from langdetect import detect as langdetect_detect

# Initialize the client with your API key
client = openai.OpenAI(api_key="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")

def record_voice(fs=44100, channels=1):
    global stop_recording
    stop_recording = False
    recorded_data = []

    def check_space_press():
        global stop_recording
        keyboard.wait('space')
        stop_recording = True
        print("Stopping recording...")

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        recorded_data.append(indata.copy())

    threading.Thread(target=check_space_press, daemon=True).start()

    with sd.InputStream(callback=callback, channels=channels, samplerate=fs) as stream:
        print("Recording... Press space to stop.")
        while not stop_recording:
            sd.sleep(100)

    if recorded_data:
        np_data = np.concatenate(recorded_data, axis=0)
        filename = Path("/home/cplisplqs/Desktop/topal/Recording.wav")
        write(filename, fs, np_data)
        print(f"Recording finished. File saved as {filename}")

def transcribe_audio_to_text(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcription.text

def detect_language(text):
    # Use langid to classify language
    lid_language, lid_confidence = langid_classify(text)
    # Use langdetect to detect language
    try:
        ldt_language = langdetect_detect(text)
    except:
        ldt_language = 'en'  # Default to English if langdetect fails

    # Simple voting mechanism to decide on language
    if lid_language == ldt_language or lid_confidence > 0.5:
        return lid_language
    return ldt_language  # Fallback or use langdetect result if confidence is low

def interact_with_chatgpt(text, language):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content

def text_to_speech(text, language):
    speech_file_path = Path("/home/cplisplqs/Desktop/topal/speech.wav")
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path

def play_audio_file(audio_path):
    os.environ['AUDIODEV'] = 'hw:1,0'
    command = ["ffplay", "-nodisp", "-autoexit", str(audio_path)]
    subprocess.run(command)
    del os.environ['AUDIODEV']

def main_loop():
    while True:
        record_voice()
        transcribed_text = transcribe_audio_to_text("/home/cplisplqs/Desktop/topal/Recording.wav")
        detected_language = detect_language(transcribed_text)
        answer = interact_with_chatgpt(transcribed_text, detected_language)
        print(f"Question: {transcribed_text}")
        speech_file_path = text_to_speech(answer, detected_language)
        print(f"Answer: {answer}")
        play_audio_file(speech_file_path)
        if input("Enter 'exit' to quit: ") == "exit":
            break

if __name__ == "__main__":
    main_loop()
