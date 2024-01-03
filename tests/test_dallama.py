import os
import subprocess

import pytest

from dallama import Model, prompt

# TODO: Need to create database via create_db.py


@pytest.fixture(scope="module", autouse=True)
def setup_prompt():
    # Setup code
    title = "foo"
    content = "baz"
    subprocess.run(f"dallama create_prompt -t '{title}' -c '{content}'", shell=True)
    yield {"title": title, "content": content}

    # Teardown code - deletes database
    if os.path.exists("db.db"):
        os.remove("db.db")


def test_prompt_creation_title(setup_prompt):
    title = setup_prompt["title"]
    row = prompt.retrieve_prompt(title)

    assert title == row["title"]


def test_prompt_creation_content(setup_prompt):
    title = setup_prompt["title"]
    content = setup_prompt["content"]
    row = prompt.retrieve_prompt(title)

    assert content == row["content"]


def test_model(setup_prompt):
    title = setup_prompt["title"]
    model = Model(base_model="llama2:7b", prompt_id=title)
    assert model.base_model == "llama2:7b"
