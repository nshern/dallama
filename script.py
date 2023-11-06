import json
import subprocess
import time
import uuid
from collections import Counter

import pandas as pd
import requests
from langdetect import detect
from nltk.tokenize import sent_tokenize
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

    print(len(results))
    title = f"res_{uuid.uuid4()}"
    print(title)

    df[title] = results

    df.to_csv("overview.csv", index=False)


def analyze_results():
    df = _read_overview()
    columns = df.columns

    for i in columns:
        if str(i).startswith("res"):
            langs_col = []
            for k in df[i]:
                langs = []
                sentences = sent_tokenize(k)
                for s in sentences:
                    try:
                        langs.append(detect(s))
                    except Exception:
                        continue
                langs_col.append(langs)

            df["langs"] = langs_col

    results = []

    for i in df["langs"]:
        count = i.count("da")
        percentage = (count / len(i)) * 100
        results.append(percentage)

    df["results"] = results

    df.to_csv("overview.csv", index=False)

    # df["langs"] = langs

    # print(df)


# TODO: Work on this
def evaluate_text(text):
    url = "https://api.languagetoolplus.com/v2/check"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "text": f"{text}",
        "language": "en-US",
        "enabledOnly": "false",
    }

    response = requests.post(url, headers=headers, data=data)

    matches = [i for i in response.json()["matches"]]

    mistakes = []
    if len(matches) > 0:
        for i in matches:
            mistakes.append(i["shortMessage"])

        count_dict = dict(Counter(mistakes))
        return count_dict

    else:
        return "None"


evaluate_text("Helo darknes my old frend")


df = _read_overview()
mistakes = []
for i in df["res_40178619-06c5-4212-9f5f-1d208f22db4c"]:
    mistakes.append(evaluate_text(i))

df["mistakes"] = mistakes

print(df)


# analyze_results()
# analyze_results()
# create_models()
# run_models()
# run_models()
# run_models()
# run_models()
