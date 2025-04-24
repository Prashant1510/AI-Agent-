# 🧠 LangChain Voice Assistant

A powerful Multimodel voice-enabled AI assistant built using Python, LangChain, google-gemini and llama2:latest. It listens to your speech, understands your question, and responds with a natural-sounding voice — just like a real assistant, It also has tools to perform different actions just my giving the voice command

---

## 🚀 Features

- 🎤 **Voice Input**: Speak directly into your microphone — no typing needed!
- 🤖 **Smart AI Response**: Uses llama2 as LLM to answer questions, search Wikipedia, and perform tasks.
- 📢 **Text-to-Speech Output**: Responds in a natural-sounding voice using `pyttsx3` with custom function.
- 🔗 **LangChain Integration**: Combines tools and agents to access real-time knowledge and context.
- 🔄 **Memory Support**: Remembers previous user queries during the session.
- 🧩 **Custom Tools**: Includes tools like Wikipedia search, time checker, weather info and more.
- 🧊 **Offline Speech-to-Text Option**: Fast recognition with speech recognizer and Google Translate for language processing.

---

## 🧠 LLM Used

- **Model**: Used open source model like Deepseek or Llama2 and paid google's gemini  (Configurable via LangChain)
- **Chain Type**: Zero-shot-react-description agent with tool integration
- **Tools Integrated**: Wikipedia, Time, Calculator, YouTube search, weather info etc. (customizable)

---

## 🗣️ Speech Recognition

- **Primary Engine**: Python's `speech_recognition` and `googletrans` for speech-to-text (online fallback)
- **Usage**: Captures live microphone input, converts speech to text in real-time

---

## 🔊 Text-to-Speech (TTS)

- **Default Engine**: Using voice of Brian (Jarvis) via a free online converter (very fast)
- **Optional Modern Voice**: Other free-to-use models like `pyttsx3`
- **Feature**: Continuously speaks assistant responses, one query at a time

---

## 🧰 Tools and Their Functions

| Tool Name             | Function                                                                 |
|-----------------------|--------------------------------------------------------------------------|
| **Time**              | Get the current time and date                                            |
| **Wikipedia**         | Search and summarize information from Wikipedia                          |
| **Web Search**        | Get real-time web results for a given topic                              |
| **YouTube**           | Search YouTube and return video links                                    |
| **Weather**           | Get weather information like temperature, wind, etc.                     |
| **Generate Llama Answer** | Generate creative responses like poems, jokes, and math solutions using Llama2 |
| **Open App**          | Open installed applications (e.g., Chrome, VS Code, Terminal, etc.)      |
| **Close App**         | Close running applications by name                                       |
| **Change Volume**     | Set the system volume to a specific percentage (0–100%)                  |
| **Set Brightness**    | Adjust screen brightness by percentage (0–100%)                          |

---

## ⚠️ Requirements

> **Note**: You can run the program on CPU, but it needs a minimum of **16 GB RAM** and processors like **Ryzen 7** or **Intel i7 and above**. GPU will boost performance if available.
