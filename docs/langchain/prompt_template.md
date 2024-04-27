# Prompt Templates

LangChain allows you to design modular prompts for your chatbot with prompt templates. Quoting LangChain’s documentation, you can think of prompt templates as predefined recipes for generating prompts for language models.

Suppose you want to build a chatbot that answers questions about patient experiences from their reviews. Here’s what a prompt template might look like for this:

```python
from langchain.prompts import ChatPromptTemplate

review_template_str = """Your job is to use patient
reviews to answer questions about their experience at a hospital.
Use the following context to answer questions. Be as detailed
as possible, but don't make up any information that's not
from the context. If you don't know an answer, say you don't know.

{context}

{question}
"""

review_template = ChatPromptTemplate.from_template(review_template_str)

context = "I had a great stay!"
question = "Did anyone have a positive experience?"

review_template.format(context=context, question=question)

```

You first import ChatPromptTemplate and define review_template_str, which contains the instructions that you’ll pass to the model, along with the variables context and question in replacement fields that LangChain delimits with curly braces ({}). You then create a ChatPromptTemplate object from review_template_str using the class method .from_template().

With review_template instantiated, you can pass context and question into the string template with review_template.format(). The results may look like you’ve done nothing more than standard Python string interpolation, but prompt templates have a lot of useful features that allow them to integrate with chat models.

Notice how your previous call to review_template.format() generated a string with Human at the beginning. This is because ChatPromptTemplate.from_template() assumes the string template is a human message by default. To change this, you can create more detailed prompt templates for each chat message that you want the model to process:

```python
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

review_system_template_str = """Your job is to use patient
reviews to answer questions about their experience at a
hospital. Use the following context to answer questions.
Be as detailed as possible, but don't make up any information
that's not from the context. If you don't know an answer, say
you don't know.

{context}
"""

review_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"], template=review_system_template_str
    )
)

review_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"], template="{question}"
    )
)

messages = [review_system_prompt, review_human_prompt]
review_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=messages,
)
context = "I had a great stay!"
question = "Did anyone have a positive experience?"

review_prompt_template.format_messages(context=context, question=question)

```

In this block, you import separate prompt templates for HumanMessage and SystemMessage. You then define a string, review_system_template_str, which serves as the template for a SystemMessage. Notice how you only declare a context variable in review_system_template_str.

From this, you create review_system_prompt which is a prompt template specifically for SystemMessage. Next you create a review_human_prompt for the HumanMessage. Notice how the template parameter is just a string with the question variable.

You then add review_system_prompt and review_human_prompt to a list called messages and create review_prompt_template, which is the final object that encompasses the prompt templates for both the SystemMessage and HumanMessage. Calling review_prompt_template.format_messages(context=context, question=question) generates a list with a SystemMessage and HumanMessage, which can be passed to a chat model.

To see how to combine chat models and prompt templates, you’ll build a chain with the LangChain Expression Language (LCEL). This helps you unlock LangChain’s core functionality of building modular customized interfaces over chat models.
