# # Copyright (c) Microsoft Corporation. All rights reserved.
# # Licensed under the MIT License.

# # -*- coding: utf-8 -*-

# import json
# import os
# from pprint import pprint
# import requests

# """
# This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
# Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
# """

# # Add your Bing Search V7 subscription key and endpoint to your environment variables.
# subscription_key = "35ef7ef31c7443aea671d7b390d7029b"
# endpoint = "https://api.bing.microsoft.com/v7.0/spellcheck"


# # Construct a request
# params = {"text": "Facebok", "mode": ""}
# headers = {"Ocp-Apim-Subscription-Key": subscription_key}

# # Call the API
# try:
#     response = requests.get(endpoint, headers=headers, params=params)
#     response.raise_for_status()

#     # print("Headers:")
#     # print(response.headers)

#     print("JSON Response:")
#     print(response.status_code)
#     pprint(response.content)
# except Exception as ex:
#     raise ex


import requests
import json

api_key = "35ef7ef31c7443aea671d7b390d7029b"
example_text = "Hollo, wrld"
example_text = "Hcad er den største by i verdn"
with open("results/nous-hermes:7b.txt", "r") as f:
    example_text = f.read()
print(example_text)
endpoint = "https://api.bing.microsoft.com/v7.0/SpellCheck"

data = {"text": example_text}

params = {"mkt": "da-DK", "mode": "proof"}

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Ocp-Apim-Subscription-Key": api_key,
}

response = requests.post(endpoint, headers=headers, params=params, data=data)

json_response = response.json()
print(json.dumps(json_response, indent=4))
