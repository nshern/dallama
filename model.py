import subprocess

import pandas as pd
import randomname


class Model:
    """
    This is the Model class which serves as a template for creating /
    model objects
    """

    def __init__(
        self,
        base_model: str,
        parameters: dict = {},
        template: str = "",
        system: str = "",
        adapter: str = "",
        license: str = "",
    ):
        self.base_model = base_model
        self.parameters = parameters
        self.template = template
        self.system = system
        self.adapter = adapter
        self.license = license
        self.model_name = f"{self.base_model}_{randomname.get_name()}"

    def _create_modelfile(self, output_path):
        modelfile = ""

        modelfile += f"FROM {self.base_model}\n"

        if self.parameters:
            for key, value in self.parameters.items():
                modelfile += f"PARAMETER {key} {value}\n"

        if self.template:
            modelfile += f"TEMPLATE {self.template}\n"

        if self.system:
            modelfile += f'SYSTEM """\n{self.system}\n"""'

        if self.adapter:
            modelfile += f"ADAPTER {self.adapter}\n"

        if self.license:
            modelfile += f"LICENSE {self.license}\n"

        self.modelfile_path = f"{output_path}/{self.model_name}"

        with open(self.modelfile_path, "w") as f:
            f.write(modelfile)

    def _create_model_from_file(self):
        if self.modelfile_path:
            command = (
                f"ollama create {self.model_name} -f {self.modelfile_path}"
            )
            subprocess.run(command, shell=True)
            print("Model created")
        else:
            print(f"{self.model_name} has no associated Modelfile")

    def _write_to_overview(self):
        df = pd.read_csv("overview.csv")
        _dict = self.__dict__
        df_dictionary = pd.DataFrame([_dict])
        df = pd.concat([df, df_dictionary], ignore_index=True)

        df.to_csv("overview.csv")

    def create_model(self, output_path="./modelfiles"):
        self._create_modelfile(output_path)
        self._create_model_from_file()
        self._write_to_overview()

    def run_model(self):
        command = f"ollama run {self.model_name}"
        subprocess.run(command, shell=True)
