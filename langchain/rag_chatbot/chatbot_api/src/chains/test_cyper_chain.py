import dotenv

from hospital_cypher_chain import hospital_cypher_chain

dotenv.load_dotenv()

question = """What is the average visit duration for
emergency visits in North Carolina?"""

response = hospital_cypher_chain.invoke(question)

print(response.get("result"))

question = """Which state had the largest percent increase
           in Medicaid visits from 2022 to 2023?"""
response = hospital_cypher_chain.invoke(question)
print(response.get("result"))
