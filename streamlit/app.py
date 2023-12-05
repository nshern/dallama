import pandas as pd

from dallama import test

result_columns = []
df = pd.read_csv("some_data.csv")
for column in df.columns:
    if str(column).startswith("res_"):
        result_columns.append(column)
