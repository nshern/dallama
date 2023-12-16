import subprocess

import pandas as pd


def _get_ollama_list():
    result = subprocess.run(
        ["ollama", "list"], stdout=subprocess.PIPE, text=True
    )
    output = (result.stdout).split("\n")

    return output


def _get_ids():
    output = _get_ollama_list()
    ids = []
    for i in output:
        if i != "":
            if not i.startswith("NAME"):
                ids.append(i.split("\t")[0].strip())

    return ids


def _get_modelfiles():
    ids = _get_ids()
    # Extract entire modelfiles
    modelfiles = []
    for i in ids:
        res = subprocess.run(
            ["ollama", "show", i, "--modelfile"],
            stdout=subprocess.PIPE,
            text=True,
        )
        output = res.stdout
        modelfiles.append(output)

    return modelfiles


def _get_temperatures():
    temperatures = []
    modelfiles = _get_modelfiles()
    for modelfile in modelfiles:
        lines = modelfile.split("\n")
        temperature = "0.8"
        for line in lines:
            if str(line).startswith("PARAMETER temperature"):
                temperature = str(line).split(" ")[-1]
        temperatures.append(temperature)

    return temperatures


def _get_base_models():
    base_models = []
    modelfiles = _get_modelfiles()
    for modelfile in modelfiles:
        lines = modelfile.split("\n")
        base_model = "def"
        for line in lines:
            if str(line).startswith("FROM "):
                base_model = str(line).split(" ")[-1]

        base_models.append(base_model)

    return base_models


def _get_overview():
    df = pd.DataFrame()
    df["Id"] = _get_ids()
    df["Temperature"] = _get_temperatures()
    df["Modelfile"] = _get_modelfiles()
    df["Base model"] = _get_base_models()

    return df


df = _get_overview()
