from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory

import json
import re  
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.tools import tools

# Initialize DeepSeek R1 via Ollama (correct way)
OLLAMA_API = "http://localhost:11434/api/generate"
# MODEL = "deepseek-r1:7b"
MODEL = "llama2:latest"



# File to store chat history
CHAT_FILE = "chat_memory/chat_history.json"

# Your custom template
# template = '''Answer the following questions as best you can. You have access to the following tools:

# {tools}

# Use the following format strictly:

# Question: the input question you must answer  
# Thought: you should always think about what to do  
# Action: the action to take, should be one of [{tool_names}]  
# Action Input: the input to the action  
# Observation: the result of the action  
# ... (this Thought/Action/Action Input/Observation can repeat maximum 2 times)  
# Thought: I now know the final answer  
# Final Answer: the final answer to the original input question  

# Do not use <tags>, markdown, or lists. Use plain text and follow the format exactly.

# Begin!

# Question: {input}  
# {agent_scratchpad}'''


# template = '''Answer the following questions as best you can. You have access to the following tools, only use tools if requires or you can give answers if you know:

# {tools}

# Use the following format very strictly and do not repeat the process give answer in one go:

# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# Final Answer: return the final answer of the question

# Begin!

# Question: {input}
# Thought:{agent_scratchpad}'''

# tools_names = "Web Search, Wikipedia,YouTube,Time"



# prompt = PromptTemplate(
#     input_variables=["input", "tool_names"],
#     template=template
# )


from langchain import hub
prompt = hub.pull("hwchase17/structured-chat-agent")


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
    # Remove <think> blocks
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Remove LaTeX formatting like \[ \]
    text = re.sub(r'\\[\[\]]', '', text)
    # Remove **bold** markers
    text = re.sub(r'\*\*', '', text)
    # Remove boxed answers \boxed{}
    text = re.sub(r'\\boxed\{.*?\}', lambda x: x.group(0)[7:-1], text)
    # Remove any remaining special characters you don't want
    text = re.sub(r'[\\*_`]', '', text)
    # Remove multiple newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


# Initialize or load chat history
chat_history = load_history()
if not chat_history:  # Add system message if new chat
    chat_history.append(SystemMessage(content="You are a helpful AI assistant."))


# Initialize the LLM
llm = OllamaLLM(model=MODEL, temperature=0.3, format="json")

# Load memory
memory = ConversationBufferMemory(return_messages=True)

# Preload memory with existing messages
for msg in chat_history:
    if isinstance(msg, HumanMessage):
        memory.chat_memory.add_user_message(msg.content)
    elif isinstance(msg, AIMessage):
        memory.chat_memory.add_ai_message(msg.content)

# tools for ai agent 
agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt,)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    max_iterations=5,
    handle_parsing_errors=True,
)

def get_response(query):
    try:
        memory.chat_memory.add_user_message(query)

        # Get the result from the agent
        result = agent_executor.invoke({"input": query})

        # Add assistant's reply to memory
        memory.chat_memory.add_ai_message(result["output"])

        # Save full chat history to file
        save_history(memory.chat_memory.messages)

        print(result)
        return clean_response(result["output"])
    except Exception as e:
        return f"Error getting response: {e}"
    


print(get_response("write a sort story on turtle and rabbit "))