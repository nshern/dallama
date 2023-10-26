import argparse
import logging
import os
import shutil

import pandas as pd

from .model import Model

logging.basicConfig(level=logging.INFO)


def ensure_ollama_on_path():
    """Check whether Ollama is on PATH and marked as executable."""
    if shutil.which("ollama") is None:
        raise FileNotFoundError("Ollama not found on system's PATH")


def _write_to_overview(model: Model):
    file_path = "~/.config/dalama/overview.csv"
    df = pd.read_csv(file_path)
    _dict = model.__dict__
    df_dictionary = pd.DataFrame([_dict])
    df = pd.concat([df, df_dictionary], ignore_index=True)

    df.to_csv(file_path)


def ensure_directory_exists():
    directory = os.path.expanduser("~/.config/dalama")

    if not os.path.isdir(directory):
        print("Config director was not found.")
        print(f"Creating config directory in {directory}...")
        os.makedirs(directory)

        if os.path.isdir(directory):
            print("Successfully created config directory")

        print("creating modelfile overview...")
        file_name = "overview.csv"
        file_path = os.path.join(directory, file_name)
        with open(file_path, "w") as file:
            file.write(
                "model_name,model_path,base_model,parameters,template,system,adapter,license,modelfile_path"
            )

    return directory


def clean(directory):
    for f in os.listdir(directory):
        os.remove(f"{directory}/{f}")


def create_prompt():
    pass


def view_models():
    df = pd.read_csv("~/.config/dalama/overview.csv")
    print(df.to_string(index=False))


def create_model(args):
    if "base_model" in args:
        base_model = args.base_model

    if "parameters" in args:
        parameters = args.parameters

    if "template" in args:
        template = args.template

    if "system" in args:
        system = args.system

    if "adapter" in args:
        adapter = args.adapter

    if "license" in args:
        license = args.license

    model = Model(
        base_model=base_model,  # type: ignore
        parameters=parameters,  # type: ignore
        template=template,  # type: ignore
        system=system,  # type: ignore
        adapter=adapter,  # type: ignore
        license=license,  # type: ignore
    )

    print("Creating model..")
    model.create_model()

    _write_to_overview(model)


def parse_args():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    clean_parser = subparser.add_parser("clean", help="delete all modelfiles")
    clean_parser.set_defaults(clean=clean)

    create_parser = subparser.add_parser("create", help="create new model")
    create_parser.add_argument("-b", "--base-model", required=True)
    create_parser.add_argument("-p", "--parameters")
    create_parser.add_argument("-t", "--template")
    create_parser.add_argument("-s", "--system")
    create_parser.add_argument("-a", "--adapter")
    create_parser.add_argument("-l", "--license")

    view_parser = subparser.add_parser("view", help="view models")
    view_parser.set_defaults(view=view_models)
    view_parser.add_argument("-n", "--names", action="store_true")

    args = parser.parse_args()

    return args


def main():
    ensure_ollama_on_path()

    directory = ensure_directory_exists()

    args = parse_args()
    print(args)

    if "clean" in args:
        clean(f"{directory}/modelfiles")

    if "base_model" in args:
        create_model(args)

    if "view" in args:
        if args.names:
            view_models(filter="names")


if __name__ == "__main__":
    main()
