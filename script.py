import json
import subprocess
import uuid

import pandas as pd
import requests
from tqdm import tqdm

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


def _read_overview():
    df = pd.read_csv("overview.csv")
    return df


def run_models():
    df = _read_overview()
    results = []

    ids = [i for i in df["id"]]

    for id in tqdm(ids):
        url = "http://localhost:11434/api/generate"
        data = {"model": id, "prompt": "."}

        response = requests.post(url, data=json.dumps(data))

        lines = response.text.splitlines()

        text = []

        for i in lines:
            r = json.loads(i)["response"]
            text.append(r)

        result = "".join(text)

        results.append(result)

    title = f"res_{uuid.uuid4()}"

    df[title] = results

    df.to_csv("overview.csv", index=False)

    # df.loc[len(df)] = new_row


# def analyze_results():


# create_models()
# run_models()
# run_models()
# run_models()
# run_models()
# run_models()
