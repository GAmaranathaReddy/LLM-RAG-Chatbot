# Build a Graph RAG Chatbot in LangChain

After all the preparatory design and data work you’ve done so far, you’re finally ready to build your chatbot! You’ll likely notice that, with the hospital system data stored in Neo4j, and the power of LangChain abstractions, building your chatbot doesn’t take much work. This is a common theme in AI and ML projects—most of the work is in design, data preparation, and deployment rather than building the AI itself.

Before you jump in, add a chatbot_api/ folder to your project with the following files and folders:

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
│   │   ├── tools/
│   │   │   └── wait_times.py
│   │
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
├── .env
└── docker-compose.yml
```

You’ll want to add a few more environment variables to your .env file as well:

```
NEO4J_URI=<YOUR_NEO4J_URI>
NEO4J_USERNAME=<YOUR_NEO4J_URI>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>

HOSPITALS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/hospitals.csv
PAYERS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/payers.csv
PHYSICIANS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/physicians.csv
PATIENTS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/patients.csv
VISITS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/visits.csv
REVIEWS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/reviews.csv

HOSPITAL_AGENT_MODEL=gpt-4-turbo
HOSPITAL_CYPHER_MODEL=gpt-4-turbo
HOSPITAL_QA_MODEL=gpt-4-turbo

```

Your .env file now includes variables that specify which LLM you’ll use for different components of your chatbot. You’ve specified these models as environment variables so that you can easily switch between different Azure OpenAI models without changing any code. Keep in mind, however, that each LLM might benefit from a unique prompting strategy, so you might need to modify your prompts if you plan on using a different suite of LLMs.

You should already have the hospital_neo4j_etl/ folder completed, and docker-compose.yml and .env are the same as before. Open up chatbot_api/pyproject.toml and add the following dependencies:

```TOML
[project]
name = "chatbot_api"
version = "0.1"
dependencies = [
    "asyncio==3.4.3",
    "fastapi==0.109.0",
    "langchain==0.1.0",
    "langchain-openai==0.0.2",
    "langchainhub==0.1.14",
    "neo4j==5.14.1",
    "numpy==1.26.2",
    "openai==1.7.2",
    "opentelemetry-api==1.22.0",
    "pydantic==2.5.1",
    "uvicorn==0.25.0"
]

[project.optional-dependencies]
dev = ["black", "flake8"]

```

You can certainly use more recent versions of these dependencies if they’re available, but keep in mind any features that might be deprecated. Open a terminal, activate your virtual environment, navigate into your chatbot_api/ folder, and install dependencies from the project’s pyproject.toml:

```shell
python -m pip install .

```

Once everything is installed, you’re ready to build the reviews chain!
