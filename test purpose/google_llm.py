from langchain_core.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

import json
import re
import sys
import os
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.tools import tools
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# File to store chat history
CHAT_FILE = "chat_memory/chat_history.json"

prompt = hub.pull("hwchase17/structured-chat-agent")

# Define the expected output schema for the tools
response_schemas = [
    ResponseSchema(name="action", description="The tool to use. Choose from: Web Search, Wikipedia, Time, YouTube."),
    ResponseSchema(name="action_input", description="The input for the tool."),
]

# Create a structured output parser
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

def load_history():
    """Load chat history from file if exists"""
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, 'r') as f:
            data = json.load(f)
            return [
                SystemMessage(**msg) if msg["type"] == "system"
                else HumanMessage(**msg) if msg["type"] == "human"
                else AIMessage(**msg)
                for msg in data
            ]
    return []

def save_history(messages):
    """Save chat history to file"""
    os.makedirs(os.path.dirname(CHAT_FILE), exist_ok=True)
    with open(CHAT_FILE, 'w') as f:
        json.dump([
            {"type": "system", "content": msg.content} if isinstance(msg, SystemMessage)
            else {"type": "human", "content": msg.content} if isinstance(msg, HumanMessage)
            else {"type": "ai", "content": msg.content}
            for msg in messages
        ], f, indent=2)

def clean_response(text):
    """Remove markdown formatting, LaTeX, and other special characters."""
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'\\[\[\]]', '', text)
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\\boxed\{.*?\}', lambda x: x.group(0)[7:-1], text)
    text = re.sub(r'[\\*_`]', '', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

# Initialize or load chat history
chat_history = load_history()
if not chat_history:  # Add system message if new chat
    chat_history.append(SystemMessage(content="You are a helpful AI assistant."))

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",  # <-- New lightweight model
    temperature=0.7,
    google_api_key= "AIzaSyB2Rn0KZ0Sg4p2QkqxfXhxr7gYg1TswkuQ" # Replace or load from .env
)
# Load memory
memory = ConversationBufferMemory(return_messages=True)

# Preload memory with existing messages
for msg in chat_history:
    if isinstance(msg, HumanMessage):
        memory.chat_memory.add_user_message(msg.content)
    elif isinstance(msg, AIMessage):
        memory.chat_memory.add_ai_message(msg.content)

# tools for ai agent
agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
)

def get_response(query):
    try:
        result = agent_executor.invoke({"input":query})
        save_history(memory.chat_memory.messages)
        return clean_response(result["output"])
    except Exception as e:
        return f"Error getting response: {e}"

