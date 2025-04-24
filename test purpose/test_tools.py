import wikipedia
from youtubesearchpython import VideosSearch
from langchain_community.tools import DuckDuckGoSearchResults
from datetime import datetime


# print(wikipedia.summary("Nikola Tesla", sentences=2))

# query = "Nikola tesla"
# videosSearch = VideosSearch(query, limit=1)
# result = videosSearch.result()["result"][0]
# # print(f"Top YouTube Result:\nTitle: {result['title']}\nLink: {result['link']}")
# print(result)


# search = DuckDuckGoSearchResults()
# print(search.run("langchain"))

# -------------------------------------------------------------------------------------------------------------------------------------- 

# Time tool
def get_current_time_and_date(_=None) -> str:
    """Returns current date, day, and time in a single string"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d (%A) %I:%M %p")

result = get_current_time_and_date()
# print(result)
# print(type(result))

# -------------------------------------------------------------------------------------------------------------------------------------- 

# weather
import requests
# # Weather 
# def get_weather():
#     url = f"https://api.open-meteo.com/v1/forecast?latitude=26.7671918&longitude=82.9938798&current_weather=true"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         weather = data['current_weather']
#         return {
#             "temperature": weather['temperature'],
#             "windspeed": weather['windspeed'],
#             "weathercode": weather['weathercode'],
#             "time": weather['time']
#         }
#     else:
#         return {"error": "Failed to fetch weather data"}

# print(get_weather())


# -------------------------------------------------------------------------------------------------------------------------------------- 

#app o/c

import subprocess
import os
# import signal

# Open app
def open_app(app_name):
    subprocess.Popen([app_name])

# Close app by name
def close_app(app_name):
    os.system(f"pkill {app_name}")


# open_app("rhythmbox")
# close_app("brave")

# -------------------------------------------------------------------------------------------------------------------------------------- 

# volume
import os

def change_volume(percent):
    os.system(f"amixer -D pulse sset Master {percent}%")
# change_volume(70)   # Set to 70%
# change_volume(30)   # Set to 30%

# -------------------------------------------------------------------------------------------------------------------------------------- 

#brightness

import subprocess
import subprocess

def set_brightness(percent: int):
    if percent < 0 or percent > 100:
        print("Brightness must be between 0 and 100.")
        return
    try:
        command = f"sudo brightnessctl set {percent}%"
        subprocess.run(command.split(), check=True)
        print(f"Brightness set to {percent}%")
    except subprocess.CalledProcessError as e:
        print("Failed to set brightness:", e)

# set_brightness(0)


str = "The sky is blue due to a phenomenon called Rayleigh scattering.  Sunlight is made up of all the colors of the rainbow.  As sunlight enters the Earth's atmosphere, it collides with tiny air molecules (mostly nitrogen and oxygen).  These molecules are much smaller than the wavelengths of visible light.  Rayleigh scattering causes shorter wavelengths of light, like blue and violet, to scatter more strongly than longer wavelengths, like red and orange.  This scattered blue light is what we see when we look at the sky.  Violet light is actually scattered even more than blue, but our eyes are more sensitive to blue, and the sun emits slightly less violet light, resulting in a blue sky."
print(len(str.split()))