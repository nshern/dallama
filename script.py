import ast
import json
import subprocess
import uuid
from typing import List

import nltk
import pandas as pd
import phunspell
import plotly.express as px
import requests
from langdetect import detect
from nltk.tokenize import sent_tokenize
from tqdm import tqdm


# This is a test
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


def _read_transposition():
    df = pd.read_csv("transposed.csv")
    return df


def run_models(iterations=1):
    print("running models")
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

    df.to_csv("data/overview.csv", index=False)


def get_results_columns():
    df = _read_overview()

    res = []

    for i in df.columns:
        if str(i).startswith("res_"):
            res.append(i)

    return res


def get_eval_columns():
    df = _read_overview()

    res = []

    for i in df.columns:
        if str(i).startswith("eval_"):
            res.append(i)

    return res


def lookup_words(words: List[str]):
    pspell = phunspell.Phunspell("da_DK")
    return pspell.lookup_list(words)


def evaluate_results():
    nltk.download("punkt")
    df = _read_overview()
    res_columns = get_results_columns()
    for res_column in tqdm(res_columns):
        eval_col_name = res_column.replace("res_", "eval_")
        misspellings = []

        for text in tqdm(df[res_column]):
            tokens = nltk.word_tokenize(text)
            foo = [token for token in tokens if token.isalpha()]
            foo = lookup_words(foo)
            misspellings.append(foo)

        df[eval_col_name] = misspellings

    df.to_csv("overview.csv", index=False)


def get_response_length():
    df = _read_overview()

    res_columns = get_results_columns()

    for res_column in res_columns:
        length_col_name = res_column.replace("res_", "len_")
        lens = []

        for text in df[res_column]:
            length = len(text)
            lens.append(length)

        df[length_col_name] = lens

    df.to_csv("overview.csv", index=False)


def count_misspellings():
    df = _read_overview()

    # TODO: Find a way to do this that is not deprecated
    df["sum_of_misspellings"] = (
        df.filter(like="eval").applymap(len).sum(axis=1)
    )

    df.to_csv("overview.csv")


def transpose():
    df = _read_overview()

    list_of_dicts = df.to_dict(orient="records")

    res = pd.DataFrame()
    for i in list_of_dicts:
        res_columns = []
        eval_columns = []
        for k in i.keys():
            if str(k).startswith("res_"):
                res_columns.append(i[k])
            if str(k).startswith("eval_"):
                eval_columns.append(i[k])

        df = pd.DataFrame()

        df["result"] = res_columns
        df["eval"] = eval_columns
        df["temperature"] = i["temperature"]
        df["base_model"] = i["base_model"]
        df["id"] = i["id"]

        res = pd.concat([df, res])

    res.to_csv("transposed.csv", index=False)


def add_calculations():
    df = _read_transposition()
    df["eval"] = df["eval"].apply(ast.literal_eval)
    df["eval_len"] = df["eval"].apply(len)

    df["res_len"] = df["result"].apply(len)

    df.to_csv("transposed.csv")


def visualize():
    df = _read_transposition()

    df["Amount of misspellings"] = df["eval_len"]
    df["Length of response"] = df["res_len"]
    # df["eval"] = df["eval"].apply(ast.literal_eval)
    # df["set_eval"] = df["eval"].apply(set)
    df["eval"] = df["eval"].apply(str.lower)
    df["set_eval"] = df["eval"].apply(lambda x: set([x]))
    df["set_eval"] = df["set_eval"].apply(list)
    # df["set_eval"] = df["set_eval"].apply(lambda x: "\n".join(x))

    formatted_list = []
    for i in df["set_eval"]:
        new_list = []

        for s in i:
            new_list.append(s + "\n")

        formatted_list.append(new_list)

    df["formatted_list"] = formatted_list
    fig = px.scatter(
        df,
        x="Amount of misspellings",
        y="Length of response",
        facet_col="temperature",
        facet_row="base_model",
        hover_data={"formatted_list": True},
    )
    fig.update_layout(margin=dict(l=50, r=50, t=50, b=50))
    fig.show()

    df.to_csv("foo.csv")


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

    # run_models(iterations)
    evaluate_results()
    get_response_length()
    count_misspellings()
    transpose()
    add_calculations()


if __name__ == "__main__":
    # main(
    #     iterations=50,
    #     fresh_run=False,
    #     models=[
    #         "llama2:7b",
    #         "llama2:13b",
    #         "mistral:7b",
    #         "mistral:7b-instruct",
    #         "starling-lm:7b",
    #         "orca-mini:13b",
    #         "orca2:7b",
    #         "orca2:13b",
    #         "neural-chat:7b",
    #         "zephyr:7b",
    #         "vicuna:7b",
    #         "vicuna:13b",
    #         "vicuna:33b",
    #         "falcon:40b",
    #         "stable-beluga:7b",
    #         "stable-beluga:13b",
    #         "wizard-vicuna:13b",
    #         "alfred:40b",
    #     ],
    #     temperatures=[0, 0.5, 1],
    # )

    # transpose()
    # add_calculations()
    # visualize()
    # df = _read_transposition()

    # fig = px.scatter(
    #     df,
    #     x="res_len",
    #     y="eval_len",
    #     facet_col="temperature",
    #     facet_row="base_model",
    # )
    # fig.show()
    # visualize()
    # evaluate_results()
    get_response_length()
    count_misspellings()
    transpose()
    add_calculations()
