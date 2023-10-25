import os
import sys

from model import Model


def clean_modelfiles(directory):
    for f in os.listdir(directory):
        os.remove(f"{directory}/{f}")


def show_models():
    pass


if __name__ == "__main__":
    if "clean" in sys.argv:
        clean_modelfiles("./modelfiles")
        sys.exit

    else:
        with open("prompt.md", "r") as f:
            prompt = f.read()

        base_models = [
            "mistral:7b",
            "mistral:7b-text-fp16",
            "llama2:7b",
            "llama2:13b",
            "vicuna:7b",
            "vicuna:13b",
            "nous-hermes:13b",
        ]

        for base_model in base_models:
            model = Model(base_model=base_model, system=prompt)
            model.create_model()
