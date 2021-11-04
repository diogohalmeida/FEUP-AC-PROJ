import pandas as pd

clients = pd.read_csv("dataset/client.csv", sep=";")

disps = pd.read_csv("dataset/disp.csv", sep=";")

# final_df.to_csv("dev/merged.csv", index=False)