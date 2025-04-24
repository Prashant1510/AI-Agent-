from modules.speech import listen
from modules.speak import speak
from modules.google_llm import get_response


def main():
    speak("Wlecome Back Sir, All Systems are ready.")
    while True:
        query = listen()
        if not query:
            continue
        query = query.lower()
        print(f"You said: {query}")

        if not query:
            continue

        if query in ["exit", "quit", "shut down", "bye", "bye-bye", "bye bye"]:
            speak("Shutting down. Sir!")
            break
        
        wake_words = ["hey", "jarvis", "hello", "bot", "listen", "hi", "hii","dude", "is", "do you", "what","who","which","tell me","can you","try","search","find","write","open","close","volume","brightness"]
        read_command = ["yes","sure","why not","please"]
        if any(word in query for word in wake_words):
            # Treat whole query as instruction
            print("\nGenerating...\n\n")

            response = get_response(query)  # Wait for response
            print(f"🤖 Agent: {response}\n")
            if response:
                word_count = len(response.split())

                if word_count <= 30:
                    speak(response)
                elif word_count > 30:
                    speak("Sir, do I also need to read it?")
                    user = listen()
                    if any(word in user for word in read_command):
                        speak(response)
                else:
                    continue


if __name__ == "__main__":
    main()