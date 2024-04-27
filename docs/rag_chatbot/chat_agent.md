# Create the Chatbot Agent

Give yourself a pat on the back if you’ve made it this far. You’ve covered a lot of information, and you’re finally ready to piece it all together and assemble the agent that will serve as your chatbot. Depending on the query you give it, your agent needs to decide between your Cypher chain, reviews chain, and wait times functions.

Start by loading your agent’s dependencies, reading in the agent model name from an environment variable, and loading a prompt template from [LangChain Hub](https://smith.langchain.com/hub):

```python
import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import (
    create_openai_functions_agent,
    Tool,
    AgentExecutor,
)
from langchain import hub
from chains.hospital_review_chain import reviews_vector_chain
from chains.hospital_cypher_chain import hospital_cypher_chain
from tools.wait_times import (
    get_current_wait_times,
    get_most_available_hospital,
)
dotenv.load_dotenv()
HOSPITAL_AGENT_MODEL = os.getenv("HOSPITAL_AGENT_MODEL")

hospital_agent_prompt = hub.pull("hwchase17/openai-functions-agent")
```

Notice how you’re importing reviews_vector_chain, hospital_cypher_chain, get_current_wait_times(), and get_most_available_hospital(). Your agent will directly use these as tools. HOSPITAL_AGENT_MODEL is the LLM that will act as your agent’s brain, deciding which tools to call and what inputs to pass them.

Instead of defining your own prompt for the agent, which you can certainly do, you load a predefined prompt from LangChain Hub. LangChain hub lets you upload, browse, pull, test, and manage prompts. In this case, the default prompt for OpenAI function agents works great.

Next, you define a list of tools your agent can use:

```python
# ...

tools = [
    Tool(
        name="Experiences",
        func=reviews_vector_chain.invoke,
        description="""Useful when you need to answer questions
        about patient experiences, feelings, or any other qualitative
        question that could be answered about a patient using semantic
        search. Not useful for answering objective questions that involve
        counting, percentages, aggregations, or listing facts. Use the
        entire prompt as input to the tool. For instance, if the prompt is
        "Are patients satisfied with their care?", the input should be
        "Are patients satisfied with their care?".
        """,
    ),
    Tool(
        name="Graph",
        func=hospital_cypher_chain.invoke,
        description="""Useful for answering questions about patients,
        physicians, hospitals, insurance payers, patient review
        statistics, and hospital visit details. Use the entire prompt as
        input to the tool. For instance, if the prompt is "How many visits
        have there been?", the input should be "How many visits have
        there been?".
        """,
    ),
    Tool(
        name="Waits",
        func=get_current_wait_times,
        description="""Use when asked about current wait times
        at a specific hospital. This tool can only get the current
        wait time at a hospital and does not have any information about
        aggregate or historical wait times. Do not pass the word "hospital"
        as input, only the hospital name itself. For example, if the prompt
        is "What is the current wait time at Jordan Inc Hospital?", the
        input should be "Jordan Inc".
        """,
    ),
    Tool(
        name="Availability",
        func=get_most_available_hospital,
        description="""
        Use when you need to find out which hospital has the shortest
        wait time. This tool does not have any information about aggregate
        or historical wait times. This tool returns a dictionary with the
        hospital name as the key and the wait time in minutes as the value.
        """,
    ),
]

```

Your agent has four tools available to it: **Experiences, Graph, Waits, and Availability**. The **Experiences** and **Graph** tools call .invoke() from their respective chains, while **Waits** and **Availability** call the wait time functions you defined. Notice that many of the tool descriptions have few-shot prompts, telling the agent when it should use the tool and providing it with an example of what inputs to pass.

As with chains, good prompt engineering is crucial for your agent’s success. You have to clearly describe each tool and how to use it so that your agent isn’t confused by a query.

The last step is to instantiate you agent:

```python
# ...

chat_model = AzureChatOpenAI(
    model=HOSPITAL_AGENT_MODEL,
    temperature=0,
)

hospital_rag_agent = create_openai_functions_agent(
    llm=chat_model,
    prompt=hospital_agent_prompt,
    tools=tools,
)

hospital_rag_agent_executor = AgentExecutor(
    agent=hospital_rag_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)

```

You first initialize a AzureChatOpenAI object using HOSPITAL_AGENT_MODEL as the LLM. You then create an AzureOpenAI functions agent with create_openai_functions_agent(). This creates an agent that’s been designed by AzureOpenAI to pass inputs to functions. It does this by returning JSON objects that store function inputs and their corresponding value.

To create the agent run time, you pass your agent and tools into AgentExecutor. Setting return_intermediate_steps and verbose to true allows you to see the agent’s thought process and the tools it calls.

With that, you’ve completed building the hospital system agent. To try it out, you’ll have to navigate into the chatbot_api/src/ folder and start a new REPL session from there.

**Note:** This is necessary because you set up relative imports in hospital_rag_agent.py that’ll later run within a Docker container. For now it means that you’ll have to start your Python interpreter only after navigating into chatbot_api/src/ for the imports to work.

You can now try out your hospital system agent on your command line:

```python
import dotenv
dotenv.load_dotenv()

from agents.hospital_rag_agent import hospital_rag_agent_executor

response = hospital_rag_agent_executor.invoke(
    {"input": "What is the wait time at Wallace-Hamilton?"}
)
print(response.get("output"))
response = hospital_rag_agent_executor.invoke(
    {"input": "Which hospital has the shortest wait time?"}
)

print(response.get("output"))
```

After loading environment variables, you ask the agent about wait times. You can see exactly what it’s doing in response to each of your queries. For instance, when you ask “What is the wait time at Wallace-Hamilton?”, it invokes the Wait tool and passes Wallace-Hamilton as input. This means the agent is calling get_current_wait_times("Wallace-Hamilton"), observing the return value, and using the return value to answer your question.

To see the agents full capabilities, you can ask it questions about patient experiences that require patient reviews to answer:

```python
response = hospital_rag_agent_executor.invoke(
    {
        "input": (
            "What have patients said about their "
            "quality of rest during their stay?"
        )
    }
)
print(response.get("output"))
```

Notice here how you never explicitly mention reviews or experiences in your question. The agent knows, based on the tool description, that it needs to invoke **Experiences**. Lastly, you can ask the agent a question requiring a Cypher query to answer:

```python
response = hospital_rag_agent_executor.invoke(
    {
        "input": (
            "Which physician has treated the "
            "most patients covered by Cigna?"
        )
    }
)

print(response.get("output"))
```

Your agent has a remarkable ability to know which tools to use and which inputs to pass based on your query. This is your fully-functioning chatbot. It has the potential to answer all the questions your stakeholders might ask based on the requirements given, and it appears to be doing a great job so far.

As you ask your chatbot more questions, you’ll almost certainly encounter situations where it calls the wrong tool or generates an incorrect answer. While modifying your prompts can help address incorrect answers, sometimes you can modify your input query to help your chatbot. Take a look at this example:

```python

response = hospital_rag_agent_executor.invoke(
    {"input": "Show me reviews written by patient 7674."}
)

print(response.get("output"))

```

In this example, you ask the agent to show you reviews written by patient 7674. Your agent invokes Experiences and doesn’t find the answer you’re looking for. While it may be possible to find the answer using semantic vector search, you can get an exact answer by generating a Cypher query to look up reviews corresponding to patient ID 7674. To help your agent understand this, you can add additional detail to your query:

```python
response = hospital_rag_agent_executor.invoke(
    {
        "input": (
            "Query the graph database to show me "
            "the reviews written by patient 7674"
        )
    }
)

response.get("output")
```

Here, you explicitly tell your agent that you want to query the graph database, which correctly invokes Graph to find the review matching patient ID 7674. Providing more detail in your queries like this is a simple yet effective way to guide your agent when it’s clearly invoking the wrong tools.

As with your reviews and Cypher chain, before placing this in front of stakeholders, you’d want to come up with a framework for evaluating your agent. The primary functionality you’d want to evaluate is the agent’s ability to call the correct tools with the correct inputs, and its ability to understand and interpret the outputs of the tools it calls.

In the final step, you’ll learn how to deploy your hospital system agent with FastAPI and Streamlit. This will make your agent accessible to anyone who calls the API endpoint or interacts with the Streamlit UI.
