# Orchestrate the Project With Docker Compose

At this point, you’ve written all the code needed to run your chatbot. This last step is to build and run your project with docker-compose. Before doing so, make sure your have all of the following files and folders in your project directory:

```
./
│
├── chatbot_api/
│   │
│   │
│   ├── src/
│   │   │
│   │   ├── agents/
│   │   │   └── hospital_rag_agent.py
│   │   │
│   │   ├── chains/
│   │   │   │
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
└── docker-compose.yml
```

Your .env file should have the following environment variables. Most of them you created earlier in this tutorial, but you’ll also need to add one new one for CHATBOT_URL so that your Streamlit app will be able to find your API:

```
....

NEO4J_URI=<YOUR_NEO4J_URI>
NEO4J_USERNAME=<YOUR_NEO4J_USERNAME>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>

HOSPITALS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/hospitals.csv
PAYERS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/payers.csv
PHYSICIANS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/physicians.csv
PATIENTS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/patients.csv
VISITS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/visits.csv
REVIEWS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/reviews.csv

HOSPITAL_AGENT_MODEL=gpt-3.5-turbo-1106
HOSPITAL_CYPHER_MODEL=gpt-3.5-turbo-1106
HOSPITAL_QA_MODEL=gpt-3.5-turbo-0125

CHATBOT_URL=http://host.docker.internal:8000/hospital-rag-agent
```

To complete your docker-compose.yml file, you’ll need to add a chatbot_frontend service. Your final docker-compose.yml file should look like this:

```

version: '3'

services:
  hospital_neo4j_etl:
    build:
      context: ./hospital_neo4j_etl
    env_file:
      - .env

  chatbot_api:
    build:
      context: ./chatbot_api
    env_file:
      - .env
    depends_on:
      - hospital_neo4j_etl
    ports:
      - "8000:8000"

  chatbot_frontend:
    build:
      context: ./chatbot_frontend
    env_file:
      - .env
    depends_on:
      - chatbot_api
    ports:
      - "8501:8501"

```

Finally, open a terminal and run:

```
docker-compose up --build
```

Once everything builds and runs, you can access the UI at http://localhost:8501/ and begin chatting with your chatbot:

![Hospital chatbot](../assets/hospital_chatbot.png 'hospital chatbot')

You’ve built a fully functioning hospital system chatbot end-to-end. Take some time to ask it questions, see the kinds of questions it’s good at answering, find out where it fails, and think about how you might improve it with better prompting or data. You can start by making sure the example questions in the sidebar are answered successfully.
