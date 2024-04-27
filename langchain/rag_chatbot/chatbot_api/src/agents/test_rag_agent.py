import dotenv

dotenv.load_dotenv()


from hospital_rag_agent import hospital_rag_agent_executor

response = hospital_rag_agent_executor.invoke(
    {"input": "What is the wait time at Wallace-Hamilton?"}
)
print(response.get("output"))
response2 = hospital_rag_agent_executor.invoke(
    {"input": "Which hospital has the shortest wait time?"}
)
print(response2.get("output"))


response = hospital_rag_agent_executor.invoke(
    {
        "input": (
            "What have patients said about their " "quality of rest during their stay?"
        )
    }
)

print(response.get("output"))

response = hospital_rag_agent_executor.invoke(
    {"input": "Show me reviews written by patient 7674."}
)
print(response.get("output"))

response = hospital_rag_agent_executor.invoke(
    {
        "input": (
            "Query the graph database to show me " "the reviews written by patient 7674"
        )
    }
)

print(response.get("output"))
