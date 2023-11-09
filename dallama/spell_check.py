import json
import os
import time

import pandas as pd
import requests


def detect_language(text):
    return detect(text)


def get_file_paths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths


def evaluate_text(file):
    api_key = ""
    endpoint = "https://api.bing.microsoft.com/v7.0/SpellCheck"

    with open(file, "r") as f:
        example_text = f.read().splitlines()

    for i in example_text:
        if i == "":
            continue

        else:
            data = {"text": i}

            params = {"mkt": "da-DK", "mode": "proof"}

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Ocp-Apim-Subscription-Key": api_key,
            }

            while True:
                response = requests.post(
                    endpoint, headers=headers, params=params, data=data
                )

                if response.status_code != 429:
                    break

                print(
                    "Rate limit exceeded. Waiting for 2 seconds before retrying.."
                )
                time.sleep(2)

            json_response = response.json()
            print(json.dumps(json_response, indent=4))
            print(detect_language(i))


if __name__ == "__main__":
    files = get_file_paths("./results")
    for file in files:
        evaluate_text(file)

    # print(detect_language("Hej mit navn er Kaj"))
