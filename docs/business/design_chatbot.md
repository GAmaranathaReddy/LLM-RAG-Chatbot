# Design the Chatbot

Now that you know the business requirements, data, and LangChain prerequisites, you’re ready to design your chatbot. A good design gives you and others a conceptual understanding of the components needed to build your chatbot. Your design should clearly illustrate how data flows through your chatbot, and it should serve as a helpful reference during development.

Your chatbot will use multiple tools to answer diverse questions about your hospital system. Here’s a flowchart illustrating how you’ll accomplish this:

![design chat](../assets/langchain_agent_design.png 'Architecture and data flow for the hospital system chatbot')

This flowchart illustrates how data moves through your chatbot, starting from the user’s input query all the way to the final response. Here’s a summary of each component:

**LangChain Agent:** The LangChain agent is the brain of your chatbot. Given a user query, the agent decides which tool to call and what to give the tool as input. The agent then observes the tool’s output and decides what to return to the user—this is the agent’s response.

**Neo4j AuraDB:** You’ll store both structured hospital system data and patient reviews in a Neo4j AuraDB graph database. You’ll learn all about this in the next section.

**LangChain Neo4j Cypher Chain:** This chain tries to convert the user query into Cypher, Neo4j’s query language, and execute the Cypher query in Neo4j. The chain then answers the user query using the Cypher query results. The chain’s response is fed back to the LangChain agent and sent to the user.

**LangChain Neo4j Reviews Vector Chain:** This is very similar to the chain you built in [Step 1](../../langchain/retrieval_objects/), except now patient review embeddings are stored in Neo4j. The chain searches for relevant reviews based on those semantically similar to the user query, and the reviews are used to answer the user query.

**Wait Times Function:** Similar to the logic in [Step 1](../../langchain/agents/), the LangChain agent tries to extract a hospital name from the user query. The hospital name is passed as input to a Python function that gets wait times, and the wait time is returned to the agent.

To walk through an example, suppose a user asks How many emergency visits were there in 2023? The LangChain agent will receive this question and decide which tool, if any, to pass the question to. In this case, the agent should pass the question to the LangChain Neo4j Cypher Chain. The chain will try to convert the question to a Cypher query, run the Cypher query in Neo4j, and use the query results to answer the question.

Once the LangChain Neo4j Cypher Chain answers the question, it will return the answer to the agent, and the agent will relay the answer to the user.

With this design in mind, you can start building your chatbot. Your first task is to set up a Neo4j AuraDB instance for your chatbot to access.
