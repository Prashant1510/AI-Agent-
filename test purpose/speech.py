import requests
import pygame
import time
import tempfile

def speak(text):

    # Fetch MP3 from the API
    url = f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={requests.utils.quote(text.strip())}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error:", response.text)
        return

    # Save to a temporary MP3 file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(response.content)
        tmp_path = tmp_file.name

    # Play using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play()

    print("🔊 Playing audio...")

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)



