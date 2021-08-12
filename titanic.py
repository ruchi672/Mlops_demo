import pandas as pd
import json
from supervised.automl import AutoML
from sklearn.metrics import accuracy_score
from flask import Flask
app = Flask(__name__)

@app.route('/api/train')
def train():
    train =pd.read_csv("titanic.csv")
    X = train[train.columns[2:]]
    print(X.head())
    y = train["Survived"]
    automl =AutoML(results_path="AutoML_titanic")
    automl.fit(X,y)
    test =pd.read_csv("titanic.csv")
    print(test.head())
    #return "hello"
    predictions = automl.predict(test)
    print(f"Accuracy: {accuracy_score(test['Survived'], predictions)*100.0:.2f}%")
    return "Dataset Trained Succesfully with Accuracy:" + f"{accuracy_score(test['Survived'], predictions)*100.0:.2f}%"

@app.route('/api/predict')
def predict():
    automl =AutoML(results_path="AutoML_titanic")
    test =pd.read_csv("titanic.csv")
    predictions = automl.predict(test)
    print(f"Accuracy: {accuracy_score(test['Survived'], predictions)*100.0:.2f}%")
    return "Dataset Trained Succesfully with Accuracy:" + f"{accuracy_score(test['Survived'], predictions)*100.0:.2f}%"

@app.route('/api/preObject')
def predictobject():
    automl =AutoML(results_path="Titanic_Model/opt/python/Titanic_Model/AutoML_titanic/")
    test =pd.read_csv("titanic.csv")
    predictions = automl.predict(test)
    test.to_json('data.json')
    with open('data.json', 'r') as example_file:
        json_obj = json.load(example_file)
        pretty_obj = json.dumps(json_obj, indent=4)
        print(pretty_obj)
        return pretty_obj

@app.route('/api/metrics')
def metrics():
    test =pd.read_csv("AutoML_titanic/leaderboard.csv")
    test.to_json('leaderboard.json')
    with open('leaderboard.json', 'r') as example_file:
        json_obj = json.load(example_file)
        pretty_obj = json.dumps(json_obj, indent=4)
        print(pretty_obj)
        return pretty_obj



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5600)
