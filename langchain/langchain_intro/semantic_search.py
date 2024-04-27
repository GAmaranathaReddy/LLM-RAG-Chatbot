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
