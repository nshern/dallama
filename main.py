import subprocess
from langchain.llms import Ollama

llms = [
    "llama2:7b",
    "llama2:13b",
    "mistral:7b",
    "vicuna:7b",
    "vicuna:13b",
    "wizard-vicuna-uncensored:7b",
    "wizard-vicuna-uncensored:13b",
    "nous-hermes:7b",
    "nous-hermes:13b",
    "mistral-openorca:7b",
]

for model_name in llms:
    subprocess.run(["ollama", "pull", model_name])

    prompt = "Hej, jeg vil have at du udelukkende svarer på dansk.\
        Du må under ingen omstændigheder tale på et andet sprog end dansk. \
        Jeg vil have at du skriver et digt om det politiske klima i Danmark i \
        1980'erne"

    llm = Ollama(model=model_name)
    res = llm.predict(prompt)

    with open(f"results/{model_name}.txt", "w") as f:
        f.write(res)

    print(f"{model_name} complete")
