import argparse
import os
from mlflow import MlflowClient
import mlflow

## for argparse
parser = argparse.ArgumentParser(description='run_id')
parser.add_argument('--run-id', type=str, help='insert run id')
args = parser.parse_args()

## set mlflow tracking uri
mlflow.set_tracking_uri("http://127.0.0.1:5000")

## download saved model
client = MlflowClient()
local_dir = '/Users/jangbs/Desktop/Test/MLOps_MLE/Model/tracking-server/artifact_downloads'
if not os.path.exists(local_dir):
    os.mkdir(local_dir)
local_path = client.download_artifacts(args.run_id, 'model', local_dir)
print("Artifacts downloaded in: {}".format(local_path))
print("Artifacts: {}".format(os.listdir(local_path)))

## load model
model = mlflow.pyfunc.load_model(local_dir+'/model')
print(model)
