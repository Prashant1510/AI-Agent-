# 🧠 LangChain Voice Assistant

A powerful voice-enabled AI assistant built using Python, LangChain, and OpenAI. It listens to your speech, understands your question, and responds with a natural-sounding voice — just like a real assistant!

---

## 🚀 Features

- 🎤 **Voice Input**: Speak directly into your microphone — no typing needed!
- 🤖 **Smart AI Response**: Uses OpenAI's LLM to answer questions, search Wikipedia, and perform tasks.
- 📢 **Text-to-Speech Output**: Responds in a natural-sounding voice using `pyttsx3` or Azure TTS.
- 🔗 **LangChain Integration**: Combines tools and agents to access real-time knowledge and context.
- 🔄 **Memory Support**: Remembers previous user queries during the session.
- 🧩 **Custom Tools**: Includes tools like Wikipedia search, time checker, and more.
- 🧊 **Offline Speech-to-Text Option**: Fast recognition with Vosk or DeepSpeech for local processing.

---

## 🧠 LLM Used

- **Model**: OpenAI GPT-3.5 / GPT-4 (Configurable via LangChain)
- **Chain Type**: Zero-shot-react-description agent with tool integration
- **Tools Integrated**: Wikipedia, Time, Calculator (customizable)

---

## 🗣️ Speech Recognition

- **Primary Engine**: Vosk (Offline) / Google Web Speech API (Online fallback)
- **Usage**: Captures live microphone input, converts speech to text in real-time

---

## 🔊 Text-to-Speech (TTS)

- **Default Engine**: `pyttsx3` (Offline)
- **Optional Modern Voice**: Azure TTS (for natural neural voices)
- **Feature**: Continuously speaks assistant responses while maintaining animation

---

## 📁 Folder Structure

