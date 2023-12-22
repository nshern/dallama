import subprocess

import pandas as pd


def test_model_creation():
    df = pd.read_csv("overview.csv")
    first = len(df)
    subprocess.run("dallama create -b llama2:7b -p gdpr -t 0.5", shell=True)
    df = pd.read_csv("overview.csv")
    second = len(df)

    assert first < second


def test_delete_model():
    df = pd.read_csv("overview.csv")
    id = list(df["id"])[-1]
    subprocess.run(f"ollama rm {id}", shell=True)
