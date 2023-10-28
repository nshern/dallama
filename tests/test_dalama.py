from dalama import Model

prompt = "You are Mario from super mario bros, acting as an assistant."

model = Model(base_model="llama2:7b", prompt=prompt, temperature="1")
