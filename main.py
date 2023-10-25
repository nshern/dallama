import glob
import os

from model import Model


def delete_all_files(directory):
    files = glob.glob(directory + "/*")
    for f in files:
        os.remove(f)


def clean_modefiles():
    delete_all_files("./modelfiles")


base_models = [
    "mistral:7b",
    "mistral:7b-text-fp16",
    "llama2:7b",
    "llama2:13b",
    "vicuna:7b",
    "vicuna:13b",
    "nous-hermes:13b",
]

if __name__ == "__main__":
    with open("prompt.md", "r") as f:
        prompt = f.read()

    for base_model in base_models:
        model = Model(base_model=base_model, system=prompt)
        model.create_modelfile("./modelfiles")
