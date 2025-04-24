from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser
from langchain.agents import AgentOutputParser
from langchain import hub
import json
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.tools import tools

# Initialize LLM via Ollama
MODEL = "llama2:latest"

# File to store chat history
CHAT_FILE = "chat_memory/chat_history.json"

# Get the structured chat prompt from LangChain Hub
prompt = hub.pull("hwchase17/structured-chat-agent")

def clean_response(text):
    """Remove markdown formatting, LaTeX, and other special characters."""
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'\\[\[\]]', '', text)
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\\boxed\{.*?\}', lambda x: x.group(0)[7:-1], text)
    text = re.sub(r'[\\*_`]', '', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

# Initialize the LLM
llm = OllamaLLM(
    model=MODEL,
    temperature=0.3,
    format="json"  # Force JSON output for better parsing
)

# Initialize memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Create agent with proper output parser
agent = create_structured_chat_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Initialize agent executor with ReActJsonSingleInputOutputParser
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=lambda error: str(error),  # Better error handling
    output_parser=ReActJsonSingleInputOutputParser()
)


def get_response(query):
    try:
        result = llm.invoke(query)
        # save_history(memory.chat_memory.messages)
        return clean_response(result)
    except Exception as e:
        return f"Error getting response: {str(e)}"

if __name__ == "__main__":
    user_query = "Write a story of turtle and rabbit "
    response = get_response(user_query)
    print(f"\nResponse: {response}\n")
 