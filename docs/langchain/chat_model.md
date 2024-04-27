# Chat Models

You might’ve guessed that the core component of LangChain is the [LLM](https://python.langchain.com/docs/modules/model_io/llms/). LangChain provides a modular interface for working with LLM providers such as OpenAI, Cohere, HuggingFace, Anthropic, Together AI, and others. In most cases, all you need is an API key from the LLM provider to get started using the LLM with LangChain. LangChain also supports LLMs or other language models hosted on your own machine.

You’ll use OpenAI for this tutorial, but keep in mind there are many great open- and closed-source providers out there. You can always test out different providers and optimize depending on your application’s needs and cost constraints.Before moving forward, make sure you’re signed up for an Azure account and you have a valid azure API keys.

```.env
AZURE_OPENAI_API_KEY="<YOUR-AZURE_API_KEY>"
AZURE_OPENAI_ENDPOINT="YOUR-AZURE_API_BASE"
OPENAI_API_VERSION="YOUR-AZURE_API_VERSION"
```

While you can interact directly with LLM objects in LangChain, a more common abstraction is the chat model. Chat models use LLMs under the hood, but they’re designed for conversations, and they interface with chat messages rather than raw text.

Using chat messages, you provide an LLM with additional detail about the kind of message you’re sending. All messages have role and content properties. The role tells the LLM who is sending the message, and the content is the message itself. Here are the most commonly used messages:

HumanMessage: A message from the user interacting with the language model.
AIMessage: A message from the language model.
SystemMessage: A message that tells the language model how to behave. Not all providers support the SystemMessage.
There are other messages types, like FunctionMessage and ToolMessage, but you’ll learn more about those when you build an agent.

Getting started with chat models in LangChain is straightforward. To instantiate an OpenAI chat model, navigate to langchain_intro and add the following code to chatbot.py:

```python
import dotenv
from langchain_openai import AzureChatOpenAI

dotenv.load_dotenv()
# Create an instance of Azure OpenAI
# Replace the deployment name with your own
llm = AzureChatOpenAI(
    deployment_name="gpt-4-turbo",
)
llm_response = llm.invoke("Hello, how are you?")
print(llm_response)

```

You first import dotenv and ChatOpenAI. Then you call dotenv.load_dotenv() which reads and stores environment variables from .env. By default, dotenv.load_dotenv() assumes .env is located in the current working directory, but you can pass the path to other directories if .env is located elsewhere.

You then instantiate a AzureChatOpenAI model using GPT 4 Turbo as the base LLM, and default temperature to 1 Azure OpenAI offers a diversity of models with varying price points, capabilities, and performances.

To use chat_model, open the project directory, start a Python interpreter, and run the following code:

```python
from langchain.schema.messages import HumanMessage, SystemMessage
from chatbot import chat_model

messages = [
    SystemMessage(
        content="""You're an assistant knowledgeable about
        healthcare. Only answer healthcare-related questions."""
    ),
    HumanMessage(content="What is Medicaid managed care?"),
]
llm_message_res = chat_model(messages)
print(llm_message_res)

```

In this block, you import HumanMessage and SystemMessage, as well as your chat model. You then define a list with a SystemMessage and a HumanMessage and run them through chat_model with chat_model(message). Under the hood, chat_model makes a request to an OpenAI endpoint serving gpt-4, and the results are returned as an AIMessage.

As you can see, the chat model answered What is Medicaid managed care? provided in the HumanMessage. You might be wondering what the chat model did with the SystemMessage in this context. Notice what happens when you ask the following question:

```python
messages = [
    SystemMessage(
        content="""You're an assistant knowledgeable about
        healthcare. Only answer healthcare-related questions."""
    ),
    HumanMessage(content="How do I change a tire?"),
]
llm_message_res = chat_model(messages)
print(llm_message_res)
```

As described earlier, the SystemMessage tells the model how to behave. In this case, you told the model to only answer healthcare-related questions. This is why it refuses to tell you how to change your tire. The ability to control how an LLM relates to the user through text instructions is powerful, and this is the foundation for creating customized chatbots through [prompt engineering](https://realpython.com/practical-prompt-engineering/).

While chat messages are a nice abstraction and are good for ensuring that you’re giving the LLM the right kind of message, you can also pass raw strings into chat models:

While chat messages are a nice abstraction and are good for ensuring that you’re giving the LLM the right kind of message, you can also pass raw strings into chat models:

```python
>>> chat_model.invoke("What is blood pressure?")
AIMessage(content='Blood pressure is the force exerted by
the blood against the walls of the blood vessels, particularly
the arteries, as it is pumped by the heart. It is measured in
millimeters of mercury (mmHg) and is typically expressed as two
numbers: systolic pressure over diastolic pressure. The systolic
pressure represents the force when the heart contracts and pumps
blood into the arteries, while the diastolic pressure represents
the force when the heart is at rest between beats. Blood pressure
is an important indicator of cardiovascular health and can be influenced
by various factors such as age, genetics, lifestyle, and underlying medical
conditions.')
```

In this code block, you pass the string What is blood pressure? directly to chat_model.invoke(). If you want to control the LLM’s behavior without a SystemMessage here, you can include instructions in the string input.

**_NOTE:_** In these examples, you used .invoke(), but LangChain has other methods that interact with LLMs. For instance, .stream() returns the response one token at time, and .batch() accepts a list of messages that the LLM responds to in one call.

Each method also has an analogous asynchronous method. For instance, you can run .invoke() asynchronously with ainvoke().

Next up, you’ll learn a modular way to guide your model’s response, as you did with the SystemMessage, making it easier to customize your chatbot.
