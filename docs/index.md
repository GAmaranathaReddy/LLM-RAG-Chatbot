# Build an LLM RAG Chatbot With LangChain

You’ve likely interacted with large language models (LLMs), like the ones behind OpenAI’s ChatGPT, and experienced their remarkable ability to answer questions, summarize documents, write code, and much more. While LLMs are remarkable by themselves, with a little programming knowledge, you can leverage libraries like [LangChain](https://python.langchain.com/docs/get_started/introduction) to create your own LLM-powered chatbots that can do just about anything.

In an enterprise setting, one of the most popular ways to create an LLM-powered chatbot is through retrieval-augmented generation (RAG). When you design a RAG system, you use a retrieval model to retrieve relevant information, usually from a database or corpus, and provide this retrieved information to an LLM to generate contextually relevant responses.

In this tutorial, you’ll step into the shoes of an AI engineer working for a large hospital system. You’ll build a RAG chatbot in LangChain that uses [Neo4j](https://neo4j.com/) to retrieve data about the patients, patient experiences, hospital locations, visits, insurance payers, and physicians in your hospital system.

In this tutorial, you’ll learn how to:

- Use **LangChain** to build custom **chatbots**
- **Design** a chatbot using your understanding of the business requirements and hospital system data
- Work with **graph databases**
- Set up a **Neo4j** AuraDB instance
- Build a **RAG** chatbot that retrieves both **structured** and **unstructured** data from Neo4j
- **Deploy** your chatbot with **FastAPI** and <b>Streamlit<b>.
