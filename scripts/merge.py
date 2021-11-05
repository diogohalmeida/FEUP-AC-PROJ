import pandas as pd

print("::::MERGING::::")

account = pd.read_csv("dev/account_clean.csv", sep=";")

card = pd.read_csv("dev/card_clean.csv", sep=";")

client = pd.read_csv("dev/client_clean.csv", sep=";")

disp = pd.read_csv("dev/disp_clean.csv", sep=";")

district = pd.read_csv("dev/district_clean.csv", sep=";")

loan = pd.read_csv("dev/loan_clean.csv", sep=";")

trans = pd.read_csv("dev/trans_clean.csv", sep=";")


client_disp = pd.merge(client, disp, on="client_id")
print("Merging client and disp (on='client_id') into client_disp")

client_disp_card = pd.merge(client_disp, card, on="disp_id", how="outer")
print("Merging client_disp and card (on='disp_id',how='outer') into client_disp_card")