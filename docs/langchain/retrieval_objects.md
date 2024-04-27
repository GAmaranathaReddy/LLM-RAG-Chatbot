# Retrieval Objects

The goal of review_chain is to answer questions about patient experiences in the hospital from their reviews. So far, you’ve manually passed reviews in as context for the question. While this can work for a small number of reviews, it doesn’t scale well. Moreover, even if you can fit all reviews into the model’s context window, there’s no guarantee it will use the correct reviews when answering a question.

To overcome this, you need a [retriever](https://python.langchain.com/docs/modules/data_connection/). The process of retrieving relevant documents and passing them to a language model to answer questions is known as retrieval-augmented generation (RAG).

For this example, you’ll store all the reviews in a [vector database](https://en.wikipedia.org/wiki/Vector_database) called [ChromaDB](https://www.trychroma.com/). If you’re unfamiliar with this database tool and topics, then check out [Embeddings and Vector Databases](https://realpython.com/chromadb-vector-database/) with ChromaDB before continuing.

```python
poetry add chromadb
```

With this installed, you can use the following code to create a ChromaDB vector database with patient reviews:

```python
import dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

REVIEWS_CSV_PATH = "data/reviews.csv"
REVIEWS_CHROMA_PATH = "chroma_data"

dotenv.load_dotenv()

loader = CSVLoader(file_path=REVIEWS_CSV_PATH, source_column="review")
reviews = loader.load()

reviews_vector_db = Chroma.from_documents(
    reviews, OpenAIEmbeddings(), persist_directory=REVIEWS_CHROMA_PATH
)
```

In lines 2 to 4, you import the dependencies needed to create the vector database. You then define REVIEWS_CSV_PATH and REVIEWS_CHROMA_PATH, which are paths where the raw reviews data is stored and where the vector database will store data, respectively.

You’ll get an overview of the hospital system data later, but all you need to know for now is that reviews.csv stores patient reviews. The review column in reviews.csv is a string with the patient’s review.

In lines 11 and 12, you load the reviews using LangChain’s CSVLoader. In lines 14 to 16, you create a ChromaDB instance from reviews using the default Azure OpenAI embedding model, and you store the review embeddings at REVIEWS_CHROMA_PATH.

**Note:** In practice, if you’re embedding a large document, you should use a text splitter. Text splitters break the document into smaller chunks before running them through an embedding model. This is important because embedding models have a fixed-size context window, and as the size of the text grows, an embedding’s ability to accurately represent the text decreases.

For this example, you can embed each review individually because they’re relatively small.

```python
(venv) $ python langchain_intro/create_retriever.py

```

It should only take a minute or so to run, and afterwards you can start performing semantic search over the review embeddings:

```python
import dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings

REVIEWS_CHROMA_PATH = "chroma_data/"
dotenv.load_dotenv()
embd = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-ada-002",
    openai_api_version="2023-05-15",
)

reviews_vector_db = Chroma(
    persist_directory=REVIEWS_CHROMA_PATH,
    embedding_function=embd,
)

question = """Has anyone complained about
           communication with the hospital staff?"""
relevant_docs = reviews_vector_db.similarity_search(question, k=3)

print(relevant_docs[0].page_content)
print(relevant_docs[1].page_content)
print(relevant_docs[2].page_content)

```

You import the dependencies needed to call ChromaDB and specify the path to the stored ChromaDB data in REVIEWS_CHROMA_PATH. You then load environment variables using dotenv.load_dotenv() and create a new Chroma instance pointing to your vector database. Notice how you have to specify an embedding function again when connecting to your vector database. Be sure this is the same embedding function that you used to create the embeddings.

Next, you define a question and call .similarity_search() on reviews_vector_db, passing in question and k=3. This creates an embedding for the question and searches the vector database for the three most similar review embeddings to question embedding. In this case, you see three reviews where patients complained about communication, which is exactly what you asked for!

The last thing to do is add your reviews retriever to review_chain so that relevant reviews are passed to the prompt as context. Here’s how you do that:

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
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough

REVIEWS_CHROMA_PATH = "chroma_data/"

# ...

reviews_vector_db = Chroma(
    persist_directory=REVIEWS_CHROMA_PATH,
    embedding_function=OpenAIEmbeddings()
)

reviews_retriever  = reviews_vector_db.as_retriever(k=10)

review_chain = (
    {"context": reviews_retriever, "question": RunnablePassthrough()}
    | review_prompt_template
    | chat_model
    | StrOutputParser()
)
```

As before, you import ChromaDB’s dependencies, specify the path to your ChromaDB data, and instantiate a new Chroma object. You then create reviews_retriever by calling .as_retriever() on reviews_vector_db to create a retriever object that you’ll add to review_chain. Because you specified k=10, the retriever will fetch the ten reviews most similar to the user’s question.

You then add a dictionary with context and question keys to the front of review_chain. Instead of passing context in manually, review_chain will pass your question to the retriever to pull relevant reviews. Assigning question to a RunnablePassthrough object ensures the question gets passed unchanged to the next step in the chain.

You now have a fully functioning chain that can answer questions about patient experiences from their reviews. Start a new REPL session and try it out:

```python
from chatbot import review_chain

context = "I had a great stay!"
# question = "Did anyone have a positive experience?"

# llm_response = review_chain.invoke({"context": context, "question": question})
# print(llm_response)
question = """Has anyone complained about
           communication with the hospital staff?"""
review_chain_result = review_chain.invoke(question)
print(review_chain_result)

```

As you can see, you only call review_chain.invoke(question) to get retrieval-augmented answers about patient experiences from their reviews. You’ll improve upon this chain later by storing review embeddings, along with other metadata, in Neo4j.

Now that you understand chat models, prompts, chains, and retrieval, you’re ready to dive into the last LangChain concept—agents.
