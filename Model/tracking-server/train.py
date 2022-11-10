import psycopg2
import pandas as pd
from pathlib import Path
from mlflow import MlflowClient
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import svm
import mlflow
import mlflow.sklearn

## extract data from postgesql
with psycopg2.connect(
    dbname='postgres', 
    user='postgres', 
    password='#wkdqudtjs1', 
    host='localhost', # 'host.docker.internal', 
    port=5432
) as conn:

    ## SELECT from iris_data table order by id
    sql = '''SELECT * FROM(
        SELECT * FROM iris_data ORDER BY id DESC LIMIT 100
    ) sub
    ORDER by id ASC'''

    df = pd.read_sql(sql, conn)

## set train/test dataset
X = df.drop(['id', 'target'], axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

## set mlflow tracking uri
mlflow.set_tracking_uri("sqlite:///mlflow.db")

## logging experiment information
client = MlflowClient()
try: 
    experiment = client.get_experiment(1)
    print(experiment)
except:
    experiment_id = client.create_experiment(
        "test model registry",
        artifact_location = Path.cwd().joinpath("mlruns").as_uri(),
        tags = {"version" : "v1"}
    )
    client.set_experiment_tag(experiment_id, "mlflow registry", "SVM")

    experiment = client.get_experiment(experiment_id)
    print("Name: {}".format(experiment.name))
    print("Experiment_id: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Tags: {}".format(experiment.tags))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

## Model train and save
C = 1.0
kernel = 'linear'
decision_function_shape = 'ovo'
mlflow.set_experiment(experiment.name)
with mlflow.start_run():
    SVM = svm.SVC(C=C, kernel=kernel,decision_function_shape=decision_function_shape )
    SVM.fit(X_train, y_train)
    ACC = SVM.score(X_test, y_test)

    mlflow.log_param("C", C)
    mlflow.log_param("kernel", kernel)
    mlflow.log_param("decision_function_shape", decision_function_shape)
    mlflow.log_metric("Accuracy", ACC)
    mlflow.sklearn.log_model(
        sk_model = SVM, 
        artifact_path = 'model',
        registered_model_name = "sk-learn-svm" 
    )
