## Main file to create table and set values 

import psycopg2
from sklearn import datasets
import threading 
import time

## load iris data
iris = datasets.load_iris()
X = iris.data
y = iris.target
y = y.astype(float)


## set iris data
def insert_iris(list_X:list, list_y:list, i:int):
    insert_data = (
        i+1, 
        list_X[i,0],
        list_X[i,1], 
        list_X[i,2], 
        list_X[i,3], 
        list_y[i]
    )
    return insert_data

## connect postgresql
conn = psycopg2.connect(dbname='postgres', user='postgres', password='my-password', host='postgres', port=5432)
cur = conn.cursor()

## if table exists then delete table
cur.execute("DROP TABLE IF EXISTS iris_data")
conn.commit()

## for CREATE TABLE
sql = '''CREATE TABLE IF NOT EXISTS iris_data(
    id SERIAL PRIMARY KEY, 
    sepal_length_cm NUMERIC(3,1), 
    sepal_width_cm NUMERIC(3,1), 
    petal_length_cm NUMERIC(3,1), 
    petal_width_cm NUMERIC(3,1), 
    target INT
);'''

## for INSERT VALUES
insert_into = '''INSERT INTO iris_data(
    id, 
    sepal_length_cm, 
    sepal_width_cm, 
    petal_length_cm, 
    petal_width_cm, 
    target
) 
    VALUES(%s, %s, %s, %s, %s, %s)
'''

## CREATE TABLE
cur.execute(sql)
conn.commit()

## INSERT VALUES in every 5 seconds
i = 0
while i < len(y):
    cur.execute(insert_into, insert_iris(X, y, i))
    conn.commit()
    time.sleep(5)
    i += 1