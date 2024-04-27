# Project Overview

Throughout this tutorial, you’ll create a few directories that make up your final chatbot. Here’s a breakdown of each directory:

- langchain_intro/ will help you get familiar with LangChain and equip you with the tools that you need to build the chatbot you saw in the demo, and it won’t be included in your final chatbot. You’ll cover this in Step 1.

- data/ has the raw hospital system data stored as CSV files. You’ll explore this data in Step 2. In Step 3, you’ll move this data into a Neo4j database that your chatbot will query to answer questions.

- hospital_neo4j_etl/ contains a script that loads the raw data from data/ into your Neo4j database. You have to run this before building your chatbot, and you’ll learn everything you need to know about setting up a Neo4j instance in Step 3.

- chatbot_api/ is your FastAPI app that serves your chatbot as a REST endpoint, and it’s the core deliverable of this project. The chatbot_api/src/agents/ and chatbot_api/src/chains/ subdirectories contain the LangChain objects that comprise your chatbot. You’ll learn what agents and chains are later, but for now, just know that your chatbot is actually a LangChain agent composed of chains and functions.

- tests/ includes two scripts that test how fast your chatbot can answer a series of questions. This will give you a feel for how much time you save by making asynchronous requests to LLM providers like OpenAI.

- chatbot_frontend/ is your Streamlit app that interacts with the chatbot endpoint in chatbot_api/. This is the UI that you saw in the demo, and you’ll build this in Step 5.

All the environment variables needed to build and run your chatbot will be stored in a .env file. You’ll deploy the code in hospital_neo4j_etl/, chatbot_api, and chatbot_frontend as Docker containers that’ll be orchestrated with Docker Compose. If you want to experiment with the chatbot before going through the rest of this tutorial, then you can download the materials and follow the instructions in the README file to get things running:
