# Create a Neo4j Cypher Chain

As you saw in [Step 2](../../business/design_chatbot/), your Neo4j Cypher chain will accept a user’s natural language query, convert the natural language query to a Cypher query, run the Cypher query in Neo4j, and use the Cypher query results to respond to the user’s query. You’ll leverage LangChain’s [GraphCypherQAChain](https://python.langchain.com/docs/use_cases/graph/graph_cypher_qa) for this.

**Note:** Any time you allow users to query a database, as you’ll do with your Cypher chain, you need to ensure they only have necessary permissions. The Neo4j credentials you’re using in this project allow users to read, write, update, and delete data from your database.

If you were building this application for a real-world project, you’d want to create credentials that restrict your user’s permissions to reads only, preventing them from writing or deleting valuable data.

Using LLMs to generate accurate Cypher queries can be challenging, especially if you have a complicated graph. Because of this, a lot of prompt engineering is required to show your graph structure and query use-cases to the LLM. [Fine-tuning](<https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)>) an LLM to generate queries is also an option, but this requires manually curated and labeled data.

To get started creating your Cypher generation chain, import dependencies and instantiate a Neo4jGraph:

```
import os
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

HOSPITAL_QA_MODEL = os.getenv("HOSPITAL_QA_MODEL")
HOSPITAL_CYPHER_MODEL = os.getenv("HOSPITAL_CYPHER_MODEL")

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

graph.refresh_schema()

```

The Neo4jGraph object is a LangChain wrapper that allows LLMs to execute queries on your Neo4j instance. You instantiate graph using your Neo4j credentials, and you call graph.refresh_schema() to sync any recent changes to your instance.

The next and most important component of your Cypher generation chain is the prompt template. Here’s what that looks like:

```
# ...

cypher_generation_template = """
Task:
Generate Cypher query for a Neo4j graph database.

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note:
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything other than
for you to construct a Cypher statement. Do not include any text except
the generated Cypher statement. Make sure the direction of the relationship is
correct in your queries. Make sure you alias both entities and relationships
properly. Do not run any queries that would add to or delete from
the database. Make sure to alias all statements that follow as with
statement (e.g. WITH v as visit, c.billing_amount as billing_amount)
If you need to divide numbers, make sure to
filter the denominator to be non zero.

Examples:
# Who is the oldest patient and how old are they?
MATCH (p:Patient)
RETURN p.name AS oldest_patient,
       duration.between(date(p.dob), date()).years AS age
ORDER BY age DESC
LIMIT 1

# Which physician has billed the least to Cigna
MATCH (p:Payer)<-[c:COVERED_BY]-(v:Visit)-[t:TREATS]-(phy:Physician)
WHERE p.name = 'Cigna'
RETURN phy.name AS physician_name, SUM(c.billing_amount) AS total_billed
ORDER BY total_billed
LIMIT 1

# Which state had the largest percent increase in Cigna visits
# from 2022 to 2023?
MATCH (h:Hospital)<-[:AT]-(v:Visit)-[:COVERED_BY]->(p:Payer)
WHERE p.name = 'Cigna' AND v.admission_date >= '2022-01-01' AND
v.admission_date < '2024-01-01'
WITH h.state_name AS state, COUNT(v) AS visit_count,
     SUM(CASE WHEN v.admission_date >= '2022-01-01' AND
     v.admission_date < '2023-01-01' THEN 1 ELSE 0 END) AS count_2022,
     SUM(CASE WHEN v.admission_date >= '2023-01-01' AND
     v.admission_date < '2024-01-01' THEN 1 ELSE 0 END) AS count_2023
WITH state, visit_count, count_2022, count_2023,
     (toFloat(count_2023) - toFloat(count_2022)) / toFloat(count_2022) * 100
     AS percent_increase
RETURN state, percent_increase
ORDER BY percent_increase DESC
LIMIT 1

# How many non-emergency patients in North Carolina have written reviews?
MATCH (r:Review)<-[:WRITES]-(v:Visit)-[:AT]->(h:Hospital)
WHERE h.state_name = 'NC' and v.admission_type <> 'Emergency'
RETURN count(*)

String category values:
Test results are one of: 'Inconclusive', 'Normal', 'Abnormal'
Visit statuses are one of: 'OPEN', 'DISCHARGED'
Admission Types are one of: 'Elective', 'Emergency', 'Urgent'
Payer names are one of: 'Cigna', 'Blue Cross', 'UnitedHealthcare', 'Medicare',
'Aetna'

A visit is considered open if its status is 'OPEN' and the discharge date is
missing.
Use abbreviations when
filtering on hospital states (e.g. "Texas" is "TX",
"Colorado" is "CO", "North Carolina" is "NC",
"Florida" is "FL", "Georgia" is "GA", etc.)

Make sure to use IS NULL or IS NOT NULL when analyzing missing properties.
Never return embedding properties in your queries. You must never include the
statement "GROUP BY" in your query. Make sure to alias all statements that
follow as with statement (e.g. WITH v as visit, c.billing_amount as
billing_amount)
If you need to divide numbers, make sure to filter the denominator to be non
zero.

The question is:
{question}
"""

cypher_generation_prompt = PromptTemplate(
    input_variables=["schema", "question"], template=cypher_generation_template
)
```

Read the contents of cypher_generation_template carefully. Notice how you’re providing the LLM with very specific instructions on what it should and shouldn’t do when generating Cypher queries. Most importantly, you’re showing the LLM your graph’s structure with the schema parameter, some example queries, and the categorical values of a few node properties.

All of the detail you provide in your prompt template improves the LLM’s chance of generating a correct Cypher query for a given question. If you’re curious about how necessary all this detail is, try creating your own prompt template with as few details as possible. Then run questions through your Cypher chain and see whether it correctly generates Cypher queries.

From there, you can iteratively update your prompt template to correct for queries that the LLM struggles to generate, but make sure you’re also cognizant of the number of input tokens you’re using. As with your review chain, you’ll want a solid system for evaluating prompt templates and the correctness of your chain’s generated Cypher queries. However, as you’ll see, the template you have above is a great starting place.

**Note:** The above prompt template provides the LLM with four examples of valid Cypher queries for your graph. Giving the LLM a few examples and then asking it to perform a task is known as few-shot prompting, and it’s a simple yet powerful technique for improving generation accuracy.

However, [few-shot prompting]("https://realpython.com/practical-prompt-engineering/#start-engineering-your-prompts) might not be sufficient for Cypher query generation, especially if you have a complicated graph. One way to improve this is to create a vector database that embeds example user questions/queries and stores their corresponding Cypher queries as metadata.

When a user asks a question, you inject Cypher queries from semantically similar questions into the prompt, providing the LLM with the most relevant examples needed to answer the current question.

Next, you define the prompt template for the question-answer component of your chain. This template tells the LLM to use the Cypher query results to generate a nicely-formatted answer to the user’s query:

```python

# ...

qa_generation_template = """You are an assistant that takes the results
from a Neo4j Cypher query and forms a human-readable response. The
query results section contains the results of a Cypher query that was
generated based on a user's natural language question. The provided
information is authoritative, you must never doubt it or try to use
your internal knowledge to correct it. Make the answer sound like a
response to the question.

Query Results:
{context}

Question:
{question}

If the provided information is empty, say you don't know the answer.
Empty information looks like this: []

If the information is not empty, you must provide an answer using the
results. If the question involves a time duration, assume the query
results are in units of days unless otherwise specified.

When names are provided in the query results, such as hospital names,
beware  of any names that have commas or other punctuation in them.
For instance, 'Jones, Brown and Murray' is a single hospital name,
not multiple hospitals. Make sure you return any list of names in
a way that isn't ambiguous and allows someone to tell what the full
names are.

Never say you don't have the right information if there is data in
the query results. Always use the data in the query results.

Helpful Answer:
"""

qa_generation_prompt = PromptTemplate(
    input_variables=["context", "question"], template=qa_generation_template
)
```

This template requires much less detail than your Cypher generation template, and you should only have to modify it if you want the LLM to respond differently, or if you’re noticing that it’s not using the query results how you want. The last step in creating your Cypher chain is to instantiate a GraphCypherQAChain object:

```python

# ...

hospital_cypher_chain = GraphCypherQAChain.from_llm(
    cypher_llm=ChatOpenAI(model=HOSPITAL_CYPHER_MODEL, temperature=0),
    qa_llm=ChatOpenAI(model=HOSPITAL_QA_MODEL, temperature=0),
    graph=graph,
    verbose=True,
    qa_prompt=qa_generation_prompt,
    cypher_prompt=cypher_generation_prompt,
    validate_cypher=True,
    top_k=100,
)

```

Here’s a breakdown of the parameters used in GraphCypherQAChain.from_llm():

- **cypher_llm:** The LLM used to generate Cypher queries.
- **qa_llm:** The LLM used to generate an answer given Cypher query results.
- **graph:** The Neo4jGraph object that connects to your Neo4j instance.
- **verbose:** Whether intermediate steps your chain performs should be printed.
- **qa_prompt:** The prompt template for responding to questions/queries.
- **cypher_prompt:** The prompt template for generating Cypher queries.
- **validate_cypher:** If true, the Cypher query will be inspected for errors and corrected before running. Note that this doesn’t guarantee the Cypher query will be valid. Instead, it corrects simple syntax errors that are easily detectable using regular expressions.
- **top_k:** The number of query results to include in qa_prompt.

Your hospital system Cypher generation chain is ready to use! It works the same way as your reviews chain. Navigate to your project directory and start a new Python interpreter session, then give it a try:

```python
import dotenv
dotenv.load_dotenv()


from chatbot_api.src.chains.hospital_cypher_chain import (
hospital_cypher_chain
)

question = """What is the average visit duration for
emergency visits in North Carolina?"""
response = hospital_cypher_chain.invoke(question)
print(response.get("result"))
```

After loading environment variables, importing hospital_cypher_chain, and invoking it with a question, you can see the steps your chain takes to answer the question. Take a second to appreciate a few accomplishments your chain made when generating the Cypher query:

- The Cypher generation LLM understood the relationship between visits and hospitals from the provided graph schema.
- Even though you asked it about **North Carolina**, the LLM knew from the prompt to use the state abbreviation **NC**.
- The LLM knew that **admission_type** properties only have the first letter capitalized, while the **status** properties are all caps.
- The QA generation LLM knew from your prompt that the query results were in units of days.

You can experiment with all kinds of queries about the hospital system. For example, here’s a relatively challenging question to convert to Cypher:

```python
question = """Which state had the largest percent increase
           in Medicaid visits from 2022 to 2023?"""
response = hospital_cypher_chain.invoke(question)
response.get("result")
```

To answer the question Which state had the largest percent increase in Medicaid visits from 2022 to 2023?, the LLM had to generate a fairly verbose Cypher query involving multiple nodes, relationships, and filters. Nonetheless, it was able to arrive at the correct answer.

The last capability your chatbot needs is to answer questions about wait times, and that’s what you’ll cover next.
