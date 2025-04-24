from langchain_ollama import OllamaLLM
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


# Initialize the LLM
llm = OllamaLLM(model=MODEL, temperature=0.3)

def get_response_llama(query):
    try:
        result = llm.invoke(query)
        return clean_response(result)
    except Exception as e:
        return f"Error getting response: {e}"
    


# print(get_response_llama("write a joke on engineers"))