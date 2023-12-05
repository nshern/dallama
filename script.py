import json
import subprocess
import uuid
from collections import Counter
from typing import List, Optional

import pandas as pd
import requests
from langdetect import detect
from nltk.tokenize import sent_tokenize
from tqdm import tqdm

# This could be an argument
# Check if model already exists


def create_models(models: List[str], temperatures: List[float]):
    prompts = ["gdpr"]

    commands = [
        f"dallama create -b {model} -p {prompt} -t {temperature}"
        for model in models
        for prompt in prompts
        for temperature in temperatures
    ]

    for i in commands:
        subprocess.run(i, shell=True)


def _overview_is_empty():
    df = pd.read_csv("overview.csv")
    if df.shape[0] == 0:
        return True
    else:
        return False


def _clear_overview() -> None:
    print("Clearing overview")
    columns = ["id", "base_model", "prompt", "temperature", "langs", "results"]
    res = pd.DataFrame(columns=columns)

    res.to_csv("overview.csv", index=False)
    print("Overview was cleared")


def _read_overview():
    df = pd.read_csv("overview.csv")
    return df


def run_models(iterations=1):
    for i in tqdm(range(iterations)):
        df = _read_overview()
        results = []

        ids = [i for i in df["id"]]

        for id in ids:
            url = "http://localhost:11434/api/generate"
            data = {"model": id, "prompt": "."}

            response = requests.post(url, data=json.dumps(data))

            lines = response.text.splitlines()

            text = []

            for i in tqdm(lines):
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
# def evaluate_text(text):
#     url = "https://api.languagetoolplus.com/v2/check"
#     headers = {
#         "accept": "application/json",
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     data = {
#         "text": f"{text}",
#         "language": "en-US",
#         "enabledOnly": "false",
#     }

#     response = requests.post(url, headers=headers, data=data)

#     matches = [i for i in response.json()["matches"]]

#     mistakes = []
#     if len(matches) > 0:
#         for i in matches:
#             mistakes.append(i["shortMessage"])

#         count_dict = dict(Counter(mistakes))
#         return count_dict

#     else:
#         return "None"


# evaluate_text("Helo darknes my old frend")


# df = _read_overview()
# mistakes = []
# for i in df["res_40178619-06c5-4212-9f5f-1d208f22db4c"]:
#     mistakes.append(evaluate_text(i))

# df["mistakes"] = mistakes

# print(df)


# TODO: Introduce timer into mix, so that reposnse time is registered


def main(
    iterations: int,
    models: List[str] = [],
    temperatures: List[float] = [],
    fresh_run=False,
):
    if fresh_run is True:
        if models == [] or temperatures == []:
            raise Exception(
                "Models and iterations need to specified if \
                             fresh_run is set to true"
            )
        _clear_overview()
        create_models(models, temperatures)

    run_models(iterations)


if __name__ == "__main__":
    main(
        iterations=10,
        fresh_run=True,
        models=[
            "llama2:7b",
            "llama2:13b",
            "mistral:7b",
            "mistral:7b-instruct",
            "starling-lm:7b",
            "orca-mini:13b",
            "neural-chat:7b",
            "zephyr:7b",
            "vicuna:13b",
        ],
        temperatures=[0, 0.5, 1],
    )
# analyze_results()
# analyze_results()
# create_models()
# run_models()
# run_models()

# run_models()
# run_models()
