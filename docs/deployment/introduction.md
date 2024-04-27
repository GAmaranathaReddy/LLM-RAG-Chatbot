# Deploy the LangChain Agent

At long last, you have a functioning LangChain agent that serves as your hospital system chatbot. The last thing you need to do is get your chatbot in front of stakeholders. For this, you’ll deploy your chatbot as a FastAPI endpoint and create a Streamlit UI to interact with the endpoint.

Before you get started, create two new folders called chatbot_frontend/ and tests/ in your project’s root directory. You’ll also need to add some additional files and folders to chatbot_api/:

```
./
│
├── chatbot_api/
│   │
│   ├── src/
│   │   │
│   │   ├── agents/
│   │   │   └── hospital_rag_agent.py
│   │   │
│   │   ├── chains/
│   │   │   ├── hospital_cypher_chain.py
│   │   │   └── hospital_review_chain.py
│   │   │
│   │   ├── models/
│   │   │   └── hospital_rag_query.py
│   │   │
│   │   ├── tools/
│   │   │   └── wait_times.py
│   │   │
│   │   ├── utils/
│   │   │   └── async_utils.py
│   │   │
│   │   ├── entrypoint.sh
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── pyproject.toml
│
├── chatbot_frontend/
│   │
│   ├── src/
│   │   ├── entrypoint.sh
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── pyproject.toml
│
├── hospital_neo4j_etl/
│   │
│   ├── src/
│   │   ├── entrypoint.sh
│   │   └── hospital_bulk_csv_write.py
│   │
│   ├── Dockerfile
│   └── pyproject.toml
│
├── tests/
│   ├── async_agent_requests.py
│   └── sync_agent_requests.py
│
├── .env

```

You need the new files in chatbot_api to build your FastAPI app, and tests/ has two scripts to demonstrate the power of making asynchronous requests to your agent. Lastly, chatbot_frontend/ has the code for the Streamlit UI that’ll interface with your chatbot. You’ll start by creating a FastAPI application to serve your agent.
