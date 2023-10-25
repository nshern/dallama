import os

from model import Model


def clean_modelfiles(directory):
    for f in os.listdir(directory):
        os.remove(f"{directory}/{f}")


base_models = [
    "mistral:7b",
    # "mistral:7b-text-fp16",
    # "llama2:7b",
    # "llama2:13b",
    # "vicuna:7b",
    # "vicuna:13b",
    # "nous-hermes:13b",
]

if __name__ == "__main__":
    clean_modelfiles("./modelfiles")

    with open("prompt.md", "r") as f:
        prompt = f.read()

    for base_model in base_models:
        model = Model(base_model=base_model, system=prompt)
        model.create_modelfile("./modelfiles")
        model.create_model_from_file()
