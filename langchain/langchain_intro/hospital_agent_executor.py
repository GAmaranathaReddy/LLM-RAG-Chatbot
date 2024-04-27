from chatbot import hospital_agent_executor

hospital_agent = hospital_agent_executor.invoke(
    {"input": "What is the current wait time at hospital C?"}
)

hospital_agent_1 = hospital_agent_executor.invoke(
    {"input": "What have patients said about their comfort at the hospital?"}
)
print(hospital_agent)
print(hospital_agent_1)
