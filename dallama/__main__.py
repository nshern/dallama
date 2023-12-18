import argparse
import logging
import os
import shutil
import sqlite3
import subprocess
from io import StringIO

import pandas as pd

# from .model import Model
from dallama.model import Model

logging.basicConfig(level=logging.INFO)


def _read_database():
    command = ["ollama list"]

    process = subprocess.Popen(
        command, subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Command failed with error: {stderr}")
    else:
        output = StringIO(stdout)
        df = pd.read_csv(output)
        print(df.head())


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


# def write_to_database(Model):
#     conn = sqlite3.connect("../database/models.db")
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#      CREATE TABLE IF NOT EXISTS models (
#      id INTEGER PRIMARY KEY AUTOINCREMENT,
#      base_model TEXT NOT NULL,
#      prompt TEXT,
#      temperature REAL
# );
# """
#     )

#     cursor.execute(
#         """
#  INSERT INTO models (base_model, prompt, temperature) VALUES (?, ?, ?);
#  """,
#         (my_model.base_model, my_model.prompt, my_model.temperature),
#     )


# def run_benchmarking()


def parse_args():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    create_parser = subparser.add_parser("create", help="create new model")
    create_parser.add_argument("-b", "--base-model", required=True)
    create_parser.add_argument("-p", "--prompt")
    create_parser.add_argument("-t", "--temperature")

    args = parser.parse_args()

    return args


def main():
    ensure_ollama_on_path()

    # directory = ensure_directory_exists()

    args = parse_args()

    if "base_model" in args:
        create_model(args)


# if __name__ == "__main__":
# _read_database()
