

import pandas as pd
import pymysql

conn = pymysql.connect(
    host="localhost",
    user= "root",
    password="----",
    database="mahipal"
)

quary = "select * from covid"

df = pd.read_sql(quary,conn)

print(df)
conn.close()





import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline



df = df.dropna()

x = df.drop(columns=['has_covid'])
y = df['has_covid']

preprocessors = ColumnTransformer(transformers=[
    ("tnf1",OneHotEncoder(),['gender','cough','city'])
],remainder='passthrough')


model = Pipeline([
    ("preprocessor",preprocessors),
    ("classifiers",LogisticRegression())
])


model.fit(x,y)

joblib.dump(model , 'lr_model.pkl')

