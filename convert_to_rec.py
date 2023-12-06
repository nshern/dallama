import pandas as pd
import plotly.express as px

# df = px.data.tips()
# df.to_csv("tips.csv")
# df = pd.read_csv("tips.csv")
df = pd.read_csv("overview.csv")
fig = px.scatter(
    df,
    x="len_7cd53897-54bf-4d93-850f-ca21ebfba13c",
    y="sum_of_misspellings",
    # color="smoker",
    facet_col="temperature",
    facet_row="base_model",
)
fig.show()
