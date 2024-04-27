# Explore the Available Data

Before building your chatbot, you need a thorough understanding of the data it will use to respond to user queries. This will help you determine what’s feasible and how you want to structure the data so that your chatbot can easily access it. All of the data you’ll use in this article was synthetically generated, and much of it was derived from a popular [health care dataset](https://www.kaggle.com/datasets/prasad22/healthcare-dataset) on Kaggle.

In practice, the following datasets would likely be stored as tables in a SQL database, but you’ll work with CSV files to keep the focus on building the chatbot. This section will give you a detailed description of each CSV file.

You’ll need to place all CSV files that are part of this project in your data/ folder before continuing with the tutorial. Make sure that you downloaded them from the materials and placed them in your data/ folder:

## hospitals.csv

The hospitals.csv file records information on each hospital that your company manages. There 30 hospitals and three fields in this file:

- hospital_id: An integer that uniquely identifies a hospital.
- hospital_name: The hospital’s name.
- hospital_state: The state the hospital is located in.

If you’re familiar with traditional SQL databases and the [star schema](https://en.wikipedia.org/wiki/Star_schema), you can think of hospitals.csv as a [dimension table](https://en.wikipedia.org/wiki/Star_schema#Dimension_tables). Dimension tables are relatively short and contain descriptive information or attributes that provide context to the data in [fact tables](https://en.wikipedia.org/wiki/Star_schema#Fact_tables). Fact tables record events about the entities stored in dimension tables, and they tend to be longer tables.

In this case, hospitals.csv records information specific to hospitals, but you can join it to fact tables to answer questions about which patients, physicians, and payers are related to the hospital. This will be more clear when you explore visits.csv.

If you’re curious, you can inspect the first few rows of hospitals.csv using a dataframe library like [Polars](https://realpython.com/polars-python/#the-python-polars-library). Make sure Polars is [installed](https://realpython.com/polars-python/#installing-python-polars) in your [virtual environment](https://realpython.com/python-virtual-environments-a-primer/), and run the following code:

```python
import polars as pl

HOSPITAL_DATA_PATH = "/Users/i552839/Desktop/Reddy/LLM-RAG-Chatbot/LLM-RAG-Chatbot/langchain/data/hospitals.csv"
data_hospitals = pl.read_csv(HOSPITAL_DATA_PATH)

print(data_hospitals.shape)

df = data_hospitals.head()

print(df)

```

In this code block, you import Polars, define the path to hospitals.csv, read the data into a Polars DataFrame, display the shape of the data, and display the first 5 rows. This shows you, for example, that Walton, LLC hospital has an ID of 2 and is located in the state of Florida, FL.

## physicians.csv

The physicians.csv file contains data about the physicians that work for your hospital system. This dataset has the following fields:

physician_id: An integer that uniquely identifies each physician.
physician_name: The physician’s name.
physician_dob: The physician’s date of birth.
physician_grad_year: The year the physician graduated medical school.
medical_school: Where the physician attended medical school.
salary: The physician’s salary.
This data can again be thought of as a dimension table, and you can inspect the first few rows using Polars:

```python
PHYSICIAN_DATA_PATH = "data/physicians.csv"
data_physician = pl.read_csv(PHYSICIAN_DATA_PATH)

print(data_physician.shape)


print(data_physician.head())
```

As you can see from the code block, there are 500 physicians in physicians.csv. The first few rows from physicians.csv give you a feel for what the data looks like. For instance, Heather Smith has a physician ID of 3, was born on June 15, 1965, graduated medical school on June 15, 1995, attended NYU Grossman Medical School, and her salary is about $295,239.

## payers.csv

The next file, payers.csv, records information about the insurance companies that your hospitals bills for patient visits. Similar to hospitals.csv, it’s a small file with a couple fields:

payer_id: An integer that uniquely identifies each payer.
payer_name: The payer’s company name.
The only five payers in the data are Medicaid, UnitedHealthcare, Aetna, Cigna, and Blue Cross. Your stakeholders are very interested in payer activity, so payers.csv will be helpful once it’s connected to patients, hospitals, and physicians.

## reviews.csv

The reviews.csv file contains patient reviews about their experience at the hospital. It has these fields:

- review_id: An integer that uniquely identifies a review.
- visit_id: An integer that identifies the patient’s visit that the review was about.
- review: This is the free form text review left by the patient.
- physician_name: The name of the physician who treated the patient.
- hospital_name: The hospital where the patient stayed.
- patient_name: The patient’s name.

This dataset is the first one you’ve seen that contains the free text review field, and your chatbot should use this to answer questions about review details and patient experiences.

Here’s what reviews.csv looks like:

```python
REVIEWS_DATA_PATH = "data/reviews.csv"
data_reviews = pl.read_csv(REVIEWS_DATA_PATH)

print(data_reviews.shape)


print(data_reviews.head())
```

## visits.csv

The last file, visits.csv, records details about every hospital visit your company has serviced. Continuing with the star schema analogy, you can think of visits.csv as a fact table that connects hospitals, physicians, patients, and payers. Here are the fields:

- visit_id: The unique identifier of a hospital visit.
- patient_id: The ID of the patient associated with the visit.
- date_of_admission: The date the patient was admitted to the hospital.
- room_number: The patient’s room number.
- admission_type: One of ‘Elective’, ‘Emergency’, or ‘Urgent’.
- chief_complaint: A string describing the patient’s primary reason for being at the hospital.
- primary_diagnosis: A string describing the primary diagnosis made by the physician.
- treatment_description: A text summary of the treatment given by the physician.
- test_results: One of ‘Inconclusive’, ‘Normal’, or ‘Abnormal’.
- discharge_date: The date the patient was discharged from the hospital
- physician_id: The ID of the physician that treated the patient.
- hospital_id: The ID of the hospital the patient stayed at.
- payer_id: The ID of the insurance payer used by the patient.
- billing_amount: The amount of money billed to the payer for the visit.
- visit_status: One of ‘OPEN’ or ‘DISCHARGED’.

This dataset gives you everything you need to answer questions about the relationship between each hospital entity. For example, if you know a physician ID, you can use visits.csv to figure out which patients, payers, and hospitals the physician is associated with. Take a look at what visits.csv looks like in Polars:

```python
VISITS_DATA_PATH = "data/visits.csv"
data_visits = pl.read_csv(VISITS_DATA_PATH)
print(data_visits.shape)
print(data_visits.head())

```

You can see there are 9998 visits recorded along with the 15 fields described above. Notice that chief_complaint, treatment_description, and primary_diagnosis might be missing for a visit. You’ll have to keep this in mind as your stakeholders might not be aware that many visits are missing critical data—this may be a valuable insight in itself! Lastly, notice that when a visit is still open, the discharged_date will be missing.

You now have an understanding of the data you’ll use to build the chatbot your stakeholders want. To recap, the files are broken out to simulate what a traditional SQL database might look like. Every hospital, patient, physician, review, and payer are connected through visits.csv.

## Wait Times

You might have noticed there’s no data to answer questions like What is the current wait time at XYZ hospital? or Which hospital currently has the shortest wait time?. Unfortunately, the hospital system doesn’t record historical wait times. Your chatbot will have to call an API to get current wait time information. You’ll see how this works later.

With an understanding of the business requirements, available data, and LangChain functionalities, you can create a design for your chatbot.
