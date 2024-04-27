# Agents

So far, you’ve created a chain to answer questions using patient reviews. What if you want your chatbot to also answer questions about other hospital data, such as hospital wait times? Ideally, your chatbot can seamlessly switch between answering patient review and wait time questions depending on the user’s query. To accomplish this, you’ll need the following components:

1. The patient review chain you already created
2. A function that can look up wait times at a hospital
3. A way for an LLM to know when it should answer questions about patient experiences or look up wait times

To accomplish the third capability, you need an [agent](https://python.langchain.com/docs/modules/agents/).

An agent is a language model that decides on a sequence of actions to execute. Unlike chains where the sequence of actions is hard-coded, agents use a language model to determine which actions to take and in which order.

Before building the agent, create the following function to generate fake wait times for a hospital:

```python
import random
import time

def get_current_wait_time(hospital: str) -> int | str:
   """Dummy function to generate fake wait times"""

   if hospital not in ["A", "B", "C", "D"]:
       return f"Hospital {hospital} does not exist"

   # Simulate API call delay
   time.sleep(1)

   return random.randint(0, 10000)
```

In get_current_wait_time(), you pass in a hospital name, check if it’s valid, and then generate a random number to simulate a wait time. In reality, this would be some sort of database query or API call, but this will serve the same purpose for this demonstration.

You can now create an agent that decides between get_current_wait_time() and review_chain.invoke() depending on the question:

```python
import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import (
    create_openai_functions_agent,
    Tool,
    AgentExecutor,
)
from langchain import hub
from langchain_intro.tools import get_current_wait_time

# ...

tools = [
    Tool(
        name="Reviews",
        func=review_chain.invoke,
        description="""Useful when you need to answer questions
        about patient reviews or experiences at the hospital.
        Not useful for answering questions about specific visit
        details such as payer, billing, treatment, diagnosis,
        chief complaint, hospital, or physician information.
        Pass the entire question as input to the tool. For instance,
        if the question is "What do patients think about the triage system?",
        the input should be "What do patients think about the triage system?"
        """,
    ),
    Tool(
        name="Waits",
        func=get_current_wait_time,
        description="""Use when asked about current wait times
        at a specific hospital. This tool can only get the current
        wait time at a hospital and does not have any information about
        aggregate or historical wait times. This tool returns wait times in
        minutes. Do not pass the word "hospital" as input,
        only the hospital name itself. For instance, if the question is
        "What is the wait time at hospital A?", the input should be "A".
        """,
    ),
]

hospital_agent_prompt = hub.pull("hwchase17/openai-functions-agent")


hospital_agent = create_openai_functions_agent(
    llm=chat_model,
    prompt=hospital_agent_prompt,
    tools=tools,
)

hospital_agent_executor = AgentExecutor(
    agent=hospital_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)
```

In this block, you import a few additional dependencies that you’ll need to create the agent. You then define a list of [Tool](https://python.langchain.com/docs/modules/agents/tools/) objects. A Tool is an interface that an agent uses to interact with a function. For instance, the first tool is named Reviews and it calls review_chain.invoke() if the question meets the criteria of description.

Notice how description gives the agent instructions as to when it should call the tool. This is where good prompt engineering skills are paramount to ensuring the LLM calls the correct tool with the correct inputs.

The second Tool in tools is named Waits, and it calls get_current_wait_time(). Again, the agent has to know when to use the Waits tool and what inputs to pass into it depending on the description.

Next, you initialize a ChatOpenAI object using gpt-4-turbo as your language model. You then create an OpenAI functions agent with create_openai_functions_agent(). This creates an agent designed to pass inputs to functions. It does this by returning valid JSON objects that store function inputs and their corresponding value.

To create the agent run time, you pass the agent and tools into [AgentExecutor](https://python.langchain.com/docs/modules/agents/concepts#agentexecutor). Setting return_intermediate_steps and verbose to True will allow you to see the agent’s thought process and the tools it calls.

Start a new REPL session to give your new agent a spin:

```python
from chatbot import hospital_agent_executor

hospital_agent = hospital_agent_executor.invoke(
    {"input": "What is the current wait time at hospital C?"}
)

hospital_agent_1 = hospital_agent_executor.invoke(
    {"input": "What have patients said about their comfort at the hospital?"}
)
print(hospital_agent)
print(hospital_agent_1)

```

You first import the agent and then call hospital_agent_executor.invoke() with a question about a wait time. As indicated in the output, the agent knows that you’re asking about a wait time, and it passes C as input to the Waits tool. The Waits tool then calls get_current_wait_time(hospital="C") and returns the corresponding wait time to the agent. The agent then uses this wait time to generate its final output.

A similar process happens when you ask the agent about patient experience reviews, except this time the agent knows to call the Reviews tool with What have patients said about their comfort at the hospital? as input. The Reviews tool runs review_chain.invoke() using your full question as input, and the agent uses the response to generate its output.

This is a profound capability. Agents give language models the ability to perform just about any task that you can write code for. Imagine all of the amazing, and potentially dangerous, chatbots you could build with agents.

You now have all of the prerequisite LangChain knowledge needed to build a custom chatbot. Next up, you’ll put on your AI engineer hat and learn about the business requirements and data needed to build your hospital system chatbot.

All of the code you’ve written so far was intended to teach you the fundamentals of LangChain, and it won’t be included in your final chatbot. Feel free to start with an empty directory in Step 2, where you’ll begin building your chatbot.
