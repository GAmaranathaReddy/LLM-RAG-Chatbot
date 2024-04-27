import polars as pl

HOSPITAL_DATA_PATH = "data/hospitals.csv"
data_hospitals = pl.read_csv(HOSPITAL_DATA_PATH)

print(data_hospitals.shape)

df = data_hospitals.head()

print(df)

PHYSICIAN_DATA_PATH = "data/physicians.csv"
data_physician = pl.read_csv(PHYSICIAN_DATA_PATH)

print(data_physician.shape)


print(data_physician.head())


REVIEWS_DATA_PATH = "data/reviews.csv"
data_reviews = pl.read_csv(REVIEWS_DATA_PATH)

print(data_reviews.shape)


print(data_reviews.head())


VISITS_DATA_PATH = "data/visits.csv"
data_visits = pl.read_csv(VISITS_DATA_PATH)

print(data_visits.shape)


print(data_visits.head())
