import subprocess

# from dallama.__main__ import main
from dallama.database import retrieve_prompt

# from sqlalchemy import MetaData, Table, create_engine, select


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
        prompt_id: str = "",
        temperature: str = "1",
    ):
        # TODO: ID Should be based on parameters, so that we can check if it
        # already exists

        self.base_model = base_model
        self.prompt_id = prompt_id
        self.temperature = temperature
        self.model_file = f"FROM {self.base_model}\n"

        if self.prompt_id is not None:
            content = retrieve_prompt(id=self.prompt_id)
            self.prompt = content

            # TODO: Here we should look up in database instead
            # with open(f"../prompts/{self.prompt}") as f:
            #     self.prompt = f.read()
            self.model_file += f'SYSTEM """\n{self.prompt}\n"""\n'

        if self.temperature is not None:
            self.model_file += f"PARAMETER temperature {self.temperature}"

        self.id = hash(self.model_file)
        self.id = str(self.id).replace("-", "")
        model_filepath = f"tmp/{self.id}"

        with open(model_filepath, "w") as f:
            f.write(self.model_file)

        # TODO: Check if model already exists
        self.create_model(model_filepath)

        print(f"Succesfully created model {self.id}")


if __name__ == "__main__":
    model = Model(base_model="llama:7b", prompt_id="gdpr", temperature="1")
