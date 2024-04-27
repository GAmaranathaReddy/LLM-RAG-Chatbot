# Create a Neo4j Vector Chain

In [Step 1](../../langchain/introduction/), you got a hands-on introduction to LangChain by building a chain that answers questions about patient experiences using their reviews. In this section, you’ll build a similar chain except you’ll use Neo4j as your vector index.

[Vector search indexes](https://neo4j.com/docs/cypher-manual/current/indexes-for-vector-search/) were released as a public beta in Neo4j 5.11. They allow you to run semantic queries directly on your graph. This is really convenient for your chatbot because you can store review embeddings in the same place as your structured hospital system data.

In LangChain, you can use [Neo4jVector](https://python.langchain.com/docs/integrations/vectorstores/neo4jvector) to create review embeddings and the retriever needed for your chain. Here’s the code to create the reviews chain:

```python

import os

from langchain.chains import RetrievalQA
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import dotenv

dotenv.load_dotenv()

HOSPITAL_QA_MODEL = os.getenv("HOSPITAL_QA_MODEL")

embd = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-ada-002",
    openai_api_version="2023-05-15",
)

neo4j_vector_index = Neo4jVector.from_existing_graph(
    embedding=embd,
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    index_name="reviews",
    node_label="Review",
    text_node_properties=[
        "physician_name",
        "patient_name",
        "text",
        "hospital_name",
    ],
    embedding_node_property="embedding",
)

review_template = """Your job is to use patient
reviews to answer questions about their experience at
a hospital. Use the following context to answer questions.
Be as detailed as possible, but don't make up any information
that's not from the context. If you don't know an answer,
say you don't know.
{context}
"""

review_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["context"], template=review_template)
)

review_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
messages = [review_system_prompt, review_human_prompt]

review_prompt = ChatPromptTemplate(
    input_variables=["context", "question"], messages=messages
)

reviews_vector_chain = RetrievalQA.from_chain_type(
    llm=AzureChatOpenAI(model=HOSPITAL_QA_MODEL, temperature=0),
    chain_type="stuff",
    retriever=neo4j_vector_index.as_retriever(k=12),
)
reviews_vector_chain.combine_documents_chain.llm_chain.prompt = review_prompt

```

you import the dependencies needed to build your review chain with Neo4j. You load the name of the chat model you’ll use for the review chain and store it in HOSPITAL_QA_MODEL. Create the vector index in Neo4j. Here’s a breakdown of each parameter:

- **embedding:** The model used to create the embeddings—you’re using AzureOpenAIEmeddings() in this example.
- **url, username, and password:** Your Neo4j instance credentials.
- **index_name:** The name given to your vector index.
- **node_label:** The node to create embeddings for.
- **text_node_properties:** The node properties to include in the embedding.
- **embedding_node_property:** The name of the embedding node property.

Once Neo4jVector.from_existing_graph() runs, you’ll see that every Review node in Neo4j has an embedding property which is a vector representation of the physician_name, patient_name, text, and hospital_name properties. This allows you to answer questions like Which hospitals have had positive reviews? It also allows the LLM to tell you which patient and physician wrote reviews matching your question.

Create the prompt template for your review chain the same way you did in [Step 1](../../langchain/prompt_template/).

Lastly, Create your reviews vector chain using a Neo4j vector index retriever that returns 12 reviews embeddings from a similarity search. By setting chain_type to "stuff" in .from_chain_type(), you’re telling the chain to pass all 12 reviews to the prompt. You can explore other chain types in [LangChain’s documentation on chains](https://python.langchain.com/docs/modules/chains).

You’re ready to try out your new reviews chain. Navigate to the root directory of your project, start a Python interpreter, and run the following commands:

```python
import dotenv
dotenv.load_dotenv()


from chatbot_api.src.chains.hospital_review_chain import (
    reviews_vector_chain
)

query = """What have patients said about hospital efficiency?
        Mention details from specific reviews."""

response = reviews_vector_chain.invoke(query)

response.get("result")
```

In this block, you import dotenv and load environment variables from .env. You then import reviews_vector_chain from hospital_review_chain and invoke it with a question about hospital efficiency. Your chain’s response might not be identical to this, but the LLM should return a nice detailed summary, as you’ve told it to.

In this example, notice how specific patient and hospital names are mentioned in the response. This happens because you embedded hospital and patient names along with the review text, so the LLM can use this information to answer questions.

**Note:** Before moving on, you should play around with reviews_vector_chain to see how it responds to different queries. Do the responses seem correct? How might you evaluate the quality of reviews_vector_chain? You won’t learn how to evaluate RAG systems in this tutorial, but you can look at this comprehensive Python example with MLFlow to get a feel for how it’s done.

Next up, you’ll create the Cypher generation chain that you’ll use to answer queries about structured hospital system data.
