from langchain_core.tools import Tool
from langchain_community.tools import DuckDuckGoSearchResults
from datetime import datetime
import wikipedia
from youtubesearchpython import VideosSearch
import requests
import subprocess
import os
# llama2 

def get_answer_by_llama(query):
    try:
        from modules.llm_engine import get_response_llama  # import inside the function
        response = get_response_llama(query=query)
        return response
    except Exception as e:
        print(f"[Error] LLaMA failed: {e}")
        return "Sorry, I couldn't get a response from the LLaMA model."
    
# Open app
def open_app(app_name: str):
    subprocess.Popen([app_name])
    print("Opening app for you")

# Close app 
def close_app(app_name: str):
    os.system(f"pkill {app_name}")
    print("Closing app for you")


# Volume
def change_volume(percent: str):
    percent = int(percent)
    os.system(f"amixer -D pulse sset Master {percent}%")
    print(f"Volume set to {percent}%")

def set_brightness(percent: str):
    percent = int(percent)
    if percent < 0 or percent > 100:
        print("Brightness must be between 0 and 100.")
        return
    try:
        command = f"sudo brightnessctl set {percent}%"
        subprocess.run(command.split(), check=True)
        print(f"Brightness set to {percent}%")
    except subprocess.CalledProcessError as e:
        print("Failed to set brightness:", e)

# Weather 
def get_weather(_=None) -> str:
    url = f"https://api.open-meteo.com/v1/forecast?latitude=26.7671918&longitude=82.9938798&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['current_weather']
        return {
            "temperature": weather['temperature'],
            "windspeed": weather['windspeed'],
            "weathercode": weather['weathercode'],
            "time": weather['time']
        }
    else:
        return {"error": "Failed to fetch weather data"}


# Time tool
def get_current_time_and_date(_=None) -> str:
    """Returns current date, day, and time in a single string"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d (%A) %I:%M %p")


#  Wikipedia tool
def search_wikipedia(query: str):
    try:
        return wikipedia.summary(query, sentences=10)
    except:
        return "I couldn't find any information on that."

#  Web Search tool (DuckDuckGo)
def search_web(query: str):
    search = DuckDuckGoSearchResults()
    return search.run(query)

#  YouTube Search tool
def search_youtube(query: str):
    try:
        videosSearch = VideosSearch(query, limit=1)
        result = videosSearch.result()["result"][0]
        return f"Top YouTube Result:\nTitle: {result['title']}\nLink: {result['link']}"
    except:
        return "Couldn't fetch YouTube result."

# Define tools
tools = [
    Tool(name="Time", func=get_current_time_and_date, description="Useful to know only the current time and date."),
    Tool(name="Wikipedia", func=search_wikipedia, description="Useful to know about a topic using Wikipedia."),
    Tool(name="Web Search", func=search_web, description="Useful for real-time web results just by passing the topic."),
    Tool(name="YouTube", func=search_youtube, description="It is use to search videos on YouTube, you will get multiple videos links and you have to provide all the links to me"),
    Tool(name="Weather", func=get_weather, description="Search weather information like wind, temprature etc."),
    Tool(name="Generate llama answer",func=get_answer_by_llama,description="It is use to generate the answer which require creativity like (writing pome, joke, solving mathematics) by llama2:latest llm "),
    Tool(name="Opne app",func=open_app,description="It is use to open an application, you have to just pass the name of application (like brave,google-chrome for chrome browser,postman,code for Vscode,aduino,figma-linux,libreoffice,cheese for camera,gnome-control-center for settings,gnome-terminal for terminal,gedit for text editor,gnome-software for app center,nautilus for files,gnome-calculator,gnome-calendar,gnome-clocks)"),
    Tool(name="Close app",func=close_app,description="It is use to close an existing application, you have to just pass the name of application (like: brave,google-chrome for chrome,postman,code for VScode,aduino,figma-linux,libreoffice,cheese for camera,gnome-control-center for settings,gnome-terminal for terminal,gedit for text editor,gnome-software for app center,nautilus for files,gnome-calculator,gnome-calendar,gnome-clocks)"),
    Tool(name="Change volume",func=change_volume,description="It is use to change/(increse or decrease) the volume by giving the percentage(like: increase the volume to 70 percent will set the volme to 70%), you only have to pass the number between 0 and 100"),
    Tool(name="Set Brightness",func=set_brightness,description="It is use to set the brightness up to certian levels (like: change/set the brithness to 30 percent will set it to 30%), you only have to pass the number between 0 and 100")
]