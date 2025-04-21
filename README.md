# 🧠 LangChain Voice Assistant

A powerful voice-enabled AI assistant built using Python, LangChain, and llama2:latest. It listens to your speech, understands your question, and responds with a natural-sounding voice — just like a real assistant!

---

## 🚀 Features

- 🎤 **Voice Input**: Speak directly into your microphone — no typing needed!
- 🤖 **Smart AI Response**: Uses llama2 as LLM to answer questions, search Wikipedia, and perform tasks.
- 📢 **Text-to-Speech Output**: Responds in a natural-sounding voice using `pyttsx3` with custom function .
- 🔗 **LangChain Integration**: Combines tools and agents to access real-time knowledge and context.
- 🔄 **Memory Support**: Remembers previous user queries during the session.
- 🧩 **Custom Tools**: Includes tools like Wikipedia search, time checker, weather info and more.
- 🧊 **Offline Speech-to-Text Option**: Fast recognition with speach recoginzer and google translation for language processing.

---

## 🧠 LLM Used

- **Model**: Used open source model like Deepseak or Llama2  (Configurable via LangChain)
- **Chain Type**: Zero-shot-react-description agent with tool integration
- **Tools Integrated**: Wikipedia, Time, Calculator, youtube search, weather info etc (customizable)

---

## 🗣️ Speech Recognition

- **Primary Engine**: Python's speech_recognition and googletrans for speach to text (Online fallback)
- **Usage**: Captures live microphone input, converts speech to text in real-time

---

## 🔊 Text-to-Speech (TTS)

- **Default Engine**: Using voice of Brian(Jarvis) by a free online converter (very fast)
- **Optional Modern Voice**: Other free to use models for voice can be pyttsx3
- **Feature**: Continuously speaks assistant responses query one by one

---

## Note: You can run the program on CPU but it needs minimum 16 Gb of RAM and processors like Ryzen 7 or I7 above, GPU will be good(if have)

