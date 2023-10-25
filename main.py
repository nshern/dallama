import argparse
import os
import sys

from model import Model


def clean(directory):
    for f in os.listdir(directory):
        os.remove(f"{directory}/{f}")


def show_models():
    pass


def parse_args():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    clean_parser = subparser.add_parser("clean", help="delete all modelfiles")
    clean_parser.set_defaults(clean=clean)

    load_model = subparser.load_model("load", help="create new model")
    load_model.add_argument("-b", "--base-model")
    load_model.add_argument("-p", "")

    # TODO: Write out all args

    # NOTE: From ZEKA, look for inspiration:
    # show_model = subparser.show_models

    # new_parser.add_argument("-t", "--title")
    # new_parser.add_argument("-a", "--tags", default="[]")
    # new_parser.add_argument("-l", "--lang", default="en-US")
    # new_parser.add_argument("-o", "--open")

    # sync_parser = subparser.add_parser("sync", help="sync notes")
    # sync_parser.set_defaults(sync=sync)

    # clean_parser = subparser.add_parser("clean", help="clean notes")
    # clean_parser.set_defaults(clean=clean)

    # args = parser.parse_args()

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    if "clean" in args:
        clean("./modelfiles")


if __name__ == "__main__":
    if "clean" in sys.argv:
        clean_modelfiles("./modelfiles")
        sys.exit
    else:
        with open("prompt.md", "r") as f:
            prompt = f.read()

        base_models = [
            "mistral:7b",
            # "mistral:7b-text-fp16",
            # "llama2:7b",
            # "llama2:13b",
            # "vicuna:7b",
            # "vicuna:13b",
            # "nous-hermes:13b",
        ]

        for base_model in base_models:
            model = Model(base_model=base_model, system=prompt)
            model.create_model()
