import subprocess
import uuid

import pandas as pd


class Model:
    """
    This is the Model class which serves as a template for creating /
    model objects
    """

    def create_model(self):
        model_filepath = f"./tmp/{self.id}"
        command = f"ollama create {self.id} -f {model_filepath}"
        subprocess.run(command, shell=True)

    def __init__(
        self,
        base_model: str,
        prompt="",
        temperature="",
    ):
        self.id = str(uuid.uuid4())
        self.base_model = base_model
        self.prompt = prompt
        self.temperature = temperature
        self.model_file = f"FROM {self.base_model}\n"

        if self.prompt != "":
            self.model_file += f'SYSTEM:"""\n{self.prompt}'

        if self.temperature != "":
            self.model_file += f"PARAMETER {self.temperature}"

        self.create_model()

        overview = pd.read_csv("./overview.csv")

        _dict = {
            "id": self.id,
            "base_model": self.base_model,
            "prompt": self.prompt,
            "temperature": self.temperature,
        }

        df = pd.DataFrame(_dict)

        result = pd.concat([overview, df], axis=1)

        result.to_csv("./overview.csv")
