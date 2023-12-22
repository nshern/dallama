import subprocess


class Model:
    """
    This is the Model class which serves as a template for creating /
    model objects
    """

    def create_model(self, model_filepath):
        command = f"ollama create {self.id} -f {model_filepath}"
        subprocess.run(command, shell=True)
        return self

    def __init__(
        self,
        base_model: str,
        prompt: str = "",
        temperature: str = "1",
    ):
        # TODO: ID Should be based on parameters, so that we can check if it
        # already exists

        self.base_model = base_model
        self.prompt = prompt
        self.temperature = temperature
        self.model_file = f"FROM {self.base_model}\n"

        if self.prompt is not None:
            # Here we should look up in database
            with open(f"../prompts/{self.prompt}") as f:
                self.prompt = f.read()
            self.model_file += f'SYSTEM """\n{self.prompt}\n"""\n'

        if self.temperature is not None:
            self.model_file += f"PARAMETER temperature {self.temperature}"

        model_filepath = f"../tmp/{self.id}"

        with open(model_filepath, "w") as f:
            f.write(self.model_file)

        # TODO: Check if model already exists
        self.create_model(model_filepath)

        self.id = hash(self.model_file)

        print(f"Succesfully created model {self.id}")
