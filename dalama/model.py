import subprocess
import uuid

import pandas as pd


class Model:
    """
    This is the Model class which serves as a template for creating /
    model objects
    """

    def create_model(self, model_filepath):
        command = f"ollama create {self.id} -f {model_filepath}"
        subprocess.run(command, shell=True)

    def __init__(
        self,
        base_model: str,
        prompt: str = "",
        temperature: str = "1",
    ):
        # TODO: ID Should be based on parameters, so that we can check if it
        # already exists

        self.id = str(uuid.uuid4())
        self.base_model = base_model
        self.prompt = prompt
        self.temperature = temperature
        self.model_file = f"FROM {self.base_model}\n"

        if self.prompt is not None:
            with open(f"./prompts/{self.prompt}") as f:
                self.prompt = f.read()
            self.model_file += f'SYSTEM:"""\n{self.prompt}\n"""\n'

        if self.temperature is not None:
            self.model_file += f"PARAMETER temperature {self.temperature}"

        model_filepath = f"./tmp/{self.id}"

        with open(model_filepath, "w") as f:
            f.write(self.model_file)

        # TODO: Check if model already exists
        self.create_model(model_filepath)

        overview = pd.read_csv("./overview.csv")

        _dict = {
            "id": self.id,
            "base_model": self.base_model,
            "prompt": self.prompt,
            "temperature": self.temperature,
        }

        df = pd.DataFrame([_dict])

        result = pd.concat([overview, df], axis=0)

        result.to_csv("./overview.csv", index=False)

        print(f"Succesfully created model {self.id}")
