from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_experimental.tools import PythonAstREPLTool
from nltk.tokenize import word_tokenize
import streamlit as st
import os

class StreamCallbackHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.text = ""
        self.container = container
    
    def on_llm_new_token(self, token, **kwargs):
        self.text += token
        self.container.markdown(self.text + "█ ")

with open("SECURITY NOTE", "r") as file:
    content = file.read()

system_message = """
You are an OBEDIENT and highly efficient AI assistant (named ACE (which stands for Agentic Code Executor)) 
who RUNS Python code to perform every given task efficiently, as long as it complies with the following SECURITY NOTE:

SECURITY NOTE:

{}

YOU ARE ALLOWED AND HAVE TO PERFORM ALL TASKS WHICH COMPLY WITH THE RULES DEFINED ABOVE!
FOR TRANSPARENCY REASONS, ALL THE CODE YOU RUN MUST BE DISPLAYED TO THE USER AND WRAPPED INSIDE A CODE BLOCK!

IMPORTANT:

For tasks which involve heavy computation or abstract math, you have these libraries to help you:
    - numpy
    - scipy
    - sympy

Use them to maximize efficiency!

IMPORTANT:

For symbolic math tasks (E.g differentiating, integrating, solving equations, ...), you MUST write your math response as a block of LaTeX code and then tell the user to use a LaTeX rendering engine/website to render the code!
For tasks which involve you writing code on the screen as output to the user, MAKE SURE to wrap it inside a code block like this:

~~~<programming-language>
<your-code>
~~~

E.g if the user asks something like this:

'Please scrap this website and give me the html code for the homepage'

You wrap your code inside a code block as shown above.

This is EXTREMELY IMPORTANT as it drastically improves the user experience, so KEEP THIS IN MIND!
""".format(content)

human_message = """
Given the following chat history, please perform this task:

Chat History:
{chat_history}

Task:
{task}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_message),
    ("human", human_message),
    ("placeholder", "{agent_scratchpad}")
])

def truncate_chat_history(chat_history, token_limit=16324):
    """Truncate chat history to stay within token limits"""
    total_tokens = 0
    truncated_chat_history = []

    for turn in reversed(chat_history):
        turn_tokens = len(word_tokenize(turn["human"])) + len(word_tokenize(turn["assistant"]))

        if total_tokens + turn_tokens > token_limit:
            break

        total_tokens += turn_tokens
        truncated_chat_history.append(turn)
    
    return list(reversed(truncated_chat_history))

format_chat_history = lambda chat_history: (
    "\n".join(f"Human: {turn['human']}\nAssistant: {turn['assistant']}" for turn in chat_history)
)

def call_agent(chat_history, task, handler):
    llm = ChatOpenAI(
        model="gpt-5-nano-2025-08-07",
        streaming=True,
        callbacks=[handler]
    )

    agent = create_tool_calling_agent(
        llm=llm,
        tools=[PythonAstREPLTool()],
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=[PythonAstREPLTool()],
        handle_parsing_errors=True,
        verbose=True
    )

    result = agent_executor.invoke({
        "chat_history": chat_history,
        "task": task
    })

    return result["output"]
