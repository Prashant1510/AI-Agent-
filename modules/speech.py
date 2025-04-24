

# This is for vosk speech recoginition


# import pyttsx3
# import speech_recognition as sr
# from vosk import Model, KaldiRecognizer
# import pyaudio
# import json
# import os

# # Voice output setup (Jarvis-style voice)
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')

# # Try to get a male "Jarvis" voice
# for v in voices:
#     if "male" in v.name.lower() or "english" in v.name.lower():
#         engine.setProperty('voice', v.id)
#         break

# engine.setProperty('rate', 170)  # Speed

# def speak(text):
#     print("🗣️ Jarvis:", text)
#     engine.say(text)
#     engine.runAndWait()

# # Voice input (Vosk)
# model_path = "models/vosk-model-en-in-0.5"
# if not os.path.exists(model_path):
#     raise FileNotFoundError("Vosk model not found. Download it and put it in the root folder.")

# model = Model(model_path)
# recognizer = KaldiRecognizer(model, 16000)

# def listen():
#     print("🎤 Listening...")
#     mic = pyaudio.PyAudio()
#     stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
#     stream.start_stream()

#     while True:
#         data = stream.read(4096, exception_on_overflow=False)
#         if recognizer.AcceptWaveform(data):
#             result = json.loads(recognizer.Result())
#             text = result.get("text", "")
#             if text:
#                 return text.lower()




# This is for whisper ===========================================================================================

# import whisper
# import sounddevice as sd
# import numpy as np
# import tempfile
# import scipy.io.wavfile

# model = whisper.load_model("base")  # or "small", "medium", "large" if you want better accuracy

# def listen():
#     print("🎤 Listening...")
#     duration = 15  # seconds
#     fs = 44100

#     print("🎙️ Say something...")
#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
#     sd.wait()

#     # Save temp audio file
#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
#         scipy.io.wavfile.write(tmp.name, fs, recording)
#         audio_path = tmp.name

#     print("🔍 Transcribing...")
#     result = model.transcribe(audio_path)
#     return result["text"].lower()




# deepseek but for specific time 

# import whisper
# import sounddevice as sd
# import numpy as np
# import tempfile
# import scipy.io.wavfile
# import webrtcvad  # For voice activity detection
# import collections

# model = whisper.load_model("base")

# def listen():
#     print("🎤 Listening (speak now, I'll stop when you pause)...")
    
#     # Audio parameters
#     fs = 16000  # Sample rate needs to be 8000, 16000, 32000 or 48000 for webrtcvad
#     frame_duration = 30  # ms
#     frame_size = int(fs * frame_duration / 1000)
    
#     # Voice activity detector (aggressiveness mode: 0-3, 3 most aggressive)
#     vad = webrtcvad.Vad(2)
    
#     # Buffer to store audio frames
#     audio_buffer = collections.deque(maxlen=100)  # Stores up to 3 seconds of audio
#     silence_frames = 0
#     speaking = False
    
#     # Minimum silence duration to stop (in frames)
#     silence_threshold = 20  # 20 frames = 600ms of silence
    
#     # Start recording
#     recording = []
    
#     def callback(indata, frames, time, status):
#         nonlocal silence_frames, speaking
        
#         # Convert to 16-bit PCM for VAD
#         audio_frame = (indata * 32767).astype(np.int16).tobytes()
        
#         # Check if frame contains speech
#         is_speech = vad.is_speech(audio_frame, fs)
        
#         if is_speech:
#             silence_frames = 0
#             speaking = True
#         elif speaking:  # Only count silence after speech has started
#             silence_frames += 1
        
#         # Store the audio
#         recording.append(indata.copy())
#         audio_buffer.append(is_speech)
        
#         # Return False to stop recording if we've had enough silence
#         if speaking and silence_frames > silence_threshold:
#             raise sd.CallbackStop
    
#     # Start streaming with callback
#     with sd.InputStream(samplerate=fs, channels=1, dtype='float32',
#                        blocksize=frame_size, callback=callback):
#         print("🎙️ Speak now...")
#         sd.sleep(10000)  # Maximum 10 seconds wait if no speech detected
    
#     if not speaking:
#         return ""
    
#     # Concatenate all recorded frames
#     audio_data = np.concatenate(recording)
    
#     # Save temp audio file
#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
#         scipy.io.wavfile.write(tmp.name, fs, (audio_data * 32767).astype(np.int16))
#         audio_path = tmp.name
    
#     print("🔍 Transcribing...")
#     result = model.transcribe(audio_path)
#     return result["text"].strip().lower()

# # # Example usage
# # if __name__ == "__main__":
# #     text = listen_until_silence()
# #     print(f"Transcribed text: {text}")


# This is new custom speech rec 

# import speech_recognition as sr
# from mtranslate import translate
# import os
# import threading
# import asyncio
# from googletrans import Translator


# # def print_loop():
# #     while True:
# #         print("Listening ...")

# async def translate_hindi_to_english(text):
#     translator = Translator()

#     result = await translator.translate(text, src='auto', dest='en')

#     return result.text

# def speech_to_text():
#     recognizer = sr.Recognizer()
#     recognizer.dynamic_energy_threshold = False
#     recognizer.energy_threshold = 34000
#     recognizer.dynamic_energy_adjustment_damping = 0.010
#     recognizer.dynamic_energy_ratio = 1.0
#     recognizer.pause_threshold = 0.3
#     recognizer.operation_timeout = None
#     recognizer.pause_threshold = 0.2
#     recognizer.non_speaking_duration = 0.2


#     with sr.Microphone() as source:

#         recognizer.adjust_for_ambient_noise(source)
#         while True:
#             print("Listening....")
#             try:
#                 audio = recognizer.listen(source,timeout=None)
#                 print("Recog...")
#                 recognizer_text = recognizer.recognize_google(audio).lower()
#                 if recognizer_text:
#                     translated_text = asyncio.run(translate_hindi_to_english(recognizer_text))
#                     return translated_text
#                 else:
#                     return ""
#             except sr.UnknownValueError:
#                 recognizer_text = ""
#             finally:
#                 print("loop end")

# stt_thread = threading.Thread(target=speech_to_text)
# # print_thread = threading.Thread(target=print_loop)
# stt_thread.start()
# # print_thread.start()
# stt_thread.join()
# # print_thread.join()


# print(speech_to_text())



# updated code: 
import speech_recognition as sr
import asyncio
from googletrans import Translator


async def translate_hindi_to_english(text):
    translator = Translator()
    result = await translator.translate(text, src='auto', dest='en')
    return result.text

async def handle_translation(text):
    translated = await translate_hindi_to_english(text)
    return translated

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 60000
    recognizer.dynamic_energy_adjustment_damping = 0.010
    recognizer.dynamic_energy_ratio = 1.0
    recognizer.pause_threshold = 0.4
    recognizer.non_speaking_duration = 0.4

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Microphone ready, start speaking...")

        
        print("Listening....")
        try:
            audio = recognizer.listen(source, timeout=None)
            print("Recognizing...")
            recognizer_text = recognizer.recognize_google(audio).lower()
            # print("You said:", recognizer_text)

            if recognizer_text:
                return asyncio.run(handle_translation(recognizer_text))
            else:
                return ""
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except Exception as e:
            print("Error:", e)
            return ""



