# Create a Chat UI With Streamlit

Your stakeholders need a way to interact with your agent without making manual API requests. To accommodate this, you’ll build a [Streamlit](https://streamlit.io/) app that acts as an interface between your stakeholders and your API. Here are the dependencies for the Streamlit UI:

```toml

[tool.poetry]
name = "chatbot_frontend"
version = "0.1"
[tool.poetry.dependencies]
requests="^2.31.0"
streamlit="^1.29.0"

[tool.poetry.group.dev.dependencies]
black = "^24.3.0"
flake8 = "^7.0.0"

```

The driving code for your Streamlit app is in chatbot_frontend/src/main.py:

```python
import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/hospital-rag-agent")

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        agent designed to answer questions about the hospitals, patients,
        visits, physicians, and insurance payers in  a fake hospital system.
        The agent uses  retrieval-augment generation (RAG) over both
        structured and unstructured data that has been synthetically generated.
        """
    )

    st.header("Example Questions")
    st.markdown("- Which hospitals are in the hospital system?")
    st.markdown("- What is the current wait time at wallace-hamilton hospital?")
    st.markdown(
        "- At which hospitals are patients complaining about billing and "
        "insurance issues?"
    )
    st.markdown("- What is the average duration in days for closed emergency visits?")
    st.markdown(
        "- What are patients saying about the nursing staff at "
        "Castaneda-Hardy?"
    )
    st.markdown("- What was the total billing amount charged to each payer for 2023?")
    st.markdown("- What is the average billing amount for medicaid visits?")
    st.markdown("- Which physician has the lowest average visit duration in days?")
    st.markdown("- How much was billed for patient 789's stay?")
    st.markdown(
        "- Which state had the largest percent increase in medicaid visits "
        "from 2022 to 2023?"
    )
    st.markdown("- What is the average billing amount per day for Aetna patients?")
    st.markdown("- How many reviews have been written from patients in Florida?")
    st.markdown(
        "- For visits that are not missing chief complaints, "
        "what percentage have reviews?"
    )
    st.markdown(
        "- What is the percentage of visits that have reviews for each hospital?"
    )
    st.markdown(
        "- Which physician has received the most reviews for this visits "
        "they've attended?"
    )
    st.markdown("- What is the ID for physician James Cooper?")
    st.markdown(
        "- List every review for visits treated by physician 270. Don't leave any out."
    )

st.title("Hospital System Chatbot")
st.info(
    "Ask me questions about patients, visits, insurance payers, hospitals, "
    "physicians, reviews, and wait times!"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )
```

Learning Streamlit is not the focus of this tutorial, so you won’t get a detailed description of this code. However, here’s a high-level overview of what this UI does:

- The entire chat history is stored and displayed each time the user makes a new query.
- The UI takes the user’s input and makes a synchronous POST request to the agent endpoint.
- The most recent agent response is displayed at the bottom of the chat and appended to the chat history.
- An explanation of how the agent generated its response it provided to the user. This is great for auditing purposes because you can see if the agent called the right tool, and you can check if the tool worked correctly.

As you’ve done, you’ll create an entrypoint file to run the UI:

```
#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo "Starting hospital chatbot frontend..."

# Run the ETL script
streamlit run main.py
```

And finally, the Docker file to create an image for the UI:

```
FROM python:3.11-slim

WORKDIR /app

COPY ./src/ /app

COPY ./pyproject.toml /code/pyproject.toml
RUN pip install /code/.

CMD ["sh", "entrypoint.sh"]
```

This Dockerfile is identical to the previous ones you’ve created. With that, you’re ready to run your entire chatbot application end-to-end.
