import argparse
import logging
import os
import shutil

# from .model import Model
from dallama.model import Model
from dallama.prompt import Prompt

logging.basicConfig(level=logging.INFO)


def ensure_ollama_on_path():
    """Check whether Ollama is on PATH and marked as executable."""
    if shutil.which("ollama") is None:
        raise FileNotFoundError("Ollama not found on system's PATH")


def ensure_directory_exists():
    directory = os.path.expanduser("~/.config/dalama")

    if not os.path.isdir(directory):
        print("Config directory was not found.")
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


def create_model(args) -> None:
    Model(
        base_model=args.base_model,
        prompt=getattr(args, "prompt", ""),
        temperature=getattr(args, "temperature", ""),
    )


# Create prompt seperate from model
# Model should reference prompt
def create_prompt(args) -> None:
    Prompt(title=args.title, content=args.content)


def parse_args():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    create_model_parser = subparser.add_parser(
        "create_model", help="create new model"
    )
    create_model_parser.add_argument("-b", "--base-model", required=True)
    create_model_parser.add_argument("-p", "--prompt")
    create_model_parser.add_argument("-t", "--temperature")

    create_prompt_parser = subparser.add_parser(
        "create prompt", help="create new prompt"
    )

    args = parser.parse_args()

    return args


def main():
    ensure_ollama_on_path()

    # directory = ensure_directory_exists()

    args = parse_args()

    if "base_model" in args:
        create_model(args)


if __name__ == "__main__":
    main()
