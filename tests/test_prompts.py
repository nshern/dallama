import os
import subprocess

import pytest

from dallama import prompt


# Deletes database after running tests
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Setup db
    title = "foo"
    content = "baz"
    subprocess.run(
        f"dallama create_prompt -t '{title}' -c '{content}'", shell=True
    )
    yield {"title": title, "content": content}

    # Teardown db
    if os.path.exists("db.db"):
        os.remove("db.db")


def test_prompt_creation_title(setup_db):
    title = setup_db["title"]
    row = prompt.retrieve_prompt(title)

    assert title == row["title"]


def test_prompt_creation_content(setup_db):
    title = setup_db["title"]
    content = setup_db["content"]
    row = prompt.retrieve_prompt(title)

    assert content == row["content"]
