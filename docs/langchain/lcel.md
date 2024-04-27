# Chains and LangChain Expression Language (LCEL)

The glue that connects chat models, prompts, and other objects in LangChain is the chain. A chain is nothing more than a sequence of calls between objects in LangChain. The recommended way to build chains is to use the LangChain Expression Language (LCEL).

To see how this works, take a look at how you’d create a chain with a chat model and prompt template:

```ptyhon
import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

dotenv.load_dotenv()

review_template_str = """Your job is to use patient
reviews to answer questions about their experience at
a hospital. Use the following context to answer questions.
Be as detailed as possible, but don't make up any information
that's not from the context. If you don't know an answer, say
you don't know.

{context}
"""

review_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"],
        template=review_template_str,
    )
)

review_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"],
        template="{question}",
    )
)
messages = [review_system_prompt, review_human_prompt]

review_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=messages,
)

chat_model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

review_chain = review_prompt_template | chat_model
```

Lines 1 to 42 are what you’ve already done. Namely, you define review_prompt_template which is a prompt template for answering questions about patient reviews, and you instantiate a gpt-4-turbo chat model. In line 44, you define review_chain with the | symbol, which is used to chain review_prompt_template and chat_model together.

This creates an object, review_chain, that can pass questions through review_prompt_template and chat_model in a single function call. In essence, this abstracts away all of the internal details of review_chain, allowing you to interact with the chain as if it were a chat model.

After saving the updated chatbot.py, start a new REPL session in your base project folder. Here’s how you can use review_chain:

```python
from langchain_intro.chatbot import review_chain

context = "I had a great stay!"
question = "Did anyone have a positive experience?"

review_chain.invoke({"context": context, "question": question})
```

In this block, you import review_chain and define context and question as before. You then pass a dictionary with the keys context and question into review_chan.invoke(). This passes context and question through the prompt template and chat model to generate an answer.

In general, the LCEL allows you to create arbitrary-length chains with the pipe symbol (|). For instance, if you wanted to format the model’s response, then you could add an output parser to the chain:

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

# ...

output_parser = StrOutputParser()

review_chain = review_prompt_template | chat_model | output_parser
```

Here, you add a StrOutputParser() instance to review_chain, which will make the model’s response more readable. Start a new REPL session and give it a try:

```python
>>> from langchain_intro.chatbot import review_chain

>>> context = "I had a great stay!"
>>> question = "Did anyone have a positive experience?"

>>> review_chain.invoke({"context": context, "question": question})
'Yes, the patient had a great stay and had a
positive experience at the hospital.'
```

This block is the same as before, except now you can see that review_chain returns a nicely-formatted string rather than an AIMessage.

The power of chains is in the creativity and flexibility they afford you. You can chain together complex pipelines to create your chatbot, and you end up with an object that executes your pipeline in a single method call. Next up, you’ll layer another object into review_chain to retrieve documents from a vector database.
