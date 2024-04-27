# Understand the Problem and Requirements

Imagine you’re an AI engineer working for a large hospital system in the US. Your stakeholders would like more visibility into the ever-changing data they collect. They want answers to ad-hoc questions about patients, visits, physicians, hospitals, and insurance payers without having to understand a query language like SQL, request a report from an analyst, or wait for someone to build a dashboard.

To accomplish this, your stakeholders want an internal chatbot tool, similar to ChatGPT, that can answer questions about your company’s data. After meeting to gather requirements, you’re provided with a list of the kinds of questions your chatbot should answer:

- What is the current wait time at XYZ hospital?
- Which hospital currently has the shortest wait time?
- At which hospitals are patients complaining about billing and insurance issues?
- Have any patients complained about the hospital being unclean?
- What have patients said about how doctors and nurses communicate with them?
- What are patients saying about the nursing staff at XYZ hospital?
- What was the total billing amount charged to [Cigna](https://en.wikipedia.org/wiki/Cigna) payers in 2023?
- How many patients has Dr. John Doe treated?
- How many visits are open and what is their average duration in days?
- Which physician has the lowest average visit duration in days?
- How much was billed for patient 789’s stay?
- Which hospital worked with the most Cigna patients in 2023?
- What’s the average billing amount for emergency visits by hospital?
- Which state had the largest percent increase inedicaid visits from 2022 to 2023?

You can answer questions like What was the total billing amount charged to Cigna payers in 2023? with aggregate statistics using a query language like SQL. Crucially, these questions have a single objective answer. You could run pre-defined queries to answer these, but any time a stakeholder has a new or slightly nuanced question, you have to write a new query. To avoid this, your chatbot should dynamically generate accurate queries.

Questions like Have any patients complained about the hospital being unclean? or What have patients said about how doctors and nurses communicate with them? are more subjective and might have many acceptable answers. Your chatbot will need to read through documents, such as patient reviews, to answer these kinds of questions.

Ultimately, your stakeholders want a single chat interface that can seamlessly answer both subjective and objective questions. This means, when presented with a question, your chatbot needs to know what type of question is being asked and which data source to pull from.

For instance, if asked How much was billed for patient 789’s stay?, your chatbot should know it needs to query a database to find the answer. If asked What have patients said about how doctors and nurses communicate with them?, your chatbot should know it needs to read and summarize patient reviews.

Next up, you’ll explore the data your hospital system records, which is arguably the most important prerequisite to building your chatbot.
