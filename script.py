import subprocess

# This could be an argument
# Check if model already exists

models = ["llama2:7b", "llama2:13b", "mistral:7b"]
prompts = ["gdpr"]
temperatures = [1, 0.5, 0]

commands = [
    f"dalama create -b {model} -p {prompt} -t {temperature}"
    for model in models
    for prompt in prompts
    for temperature in temperatures
]

for i in commands:
    subprocess.run(i, shell=True)
