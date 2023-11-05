import json
import sqlite3
import subprocess

import pandas as pd
import requests

# This could be an argument
# Check if model already exists


def create_models():
    models = ["llama2:7b", "mistral:7b"]
    prompts = ["gdpr"]
    temperatures = [1, 0.5, 0]

    commands = [
        f"dalama create -b {model} -p {prompt} -t {temperature}"
        for model in models
        for prompt in prompts
        for temperature in temperatures
    ]

    for i in commands:
        subprocess.run(i, shell=True)


def run_models(id="0426317b-ed19-4076-b44a-9ab28cbfa489"):
    url = "http://localhost:11434/api/generate"
    data = {"model": id, "prompt": "."}

    response = requests.post(url, data=json.dumps(data))

    lines = response.text.splitlines()

    text = []

    for i in lines:
        r = json.loads(i)["response"]
        text.append(r)

    result = "".join(text)
    print(result)

    new_row = {"id": id, "res": result}
    new_row = pd.Series(new_row)

    df = pd.read_csv("result_overview.csv")

    df = pd.concat([df, new_row], ignore_index=True)

    print(df)

    # df.loc[len(df)] = new_row
