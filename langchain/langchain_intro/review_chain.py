from chatbot import review_chain

context = "I had a great stay!"
# question = "Did anyone have a positive experience?"

# llm_response = review_chain.invoke({"context": context, "question": question})
# print(llm_response)
question = """Has anyone complained about
           communication with the hospital staff?"""
review_chain_result = review_chain.invoke(question)
print(review_chain_result)
