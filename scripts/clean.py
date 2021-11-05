import pandas as pd

print("::::CLEANING::::")

account = pd.read_csv("dev/account_loaded.csv", sep=";")
account.to_csv("dev/account_clean.csv", index=False)

card = pd.read_csv("dev/card_loaded.csv", sep=";")
card.to_csv("dev/card_clean.csv", index=False)

client = pd.read_csv("dev/client_loaded.csv", sep=";")
client.to_csv("dev/client_clean.csv", index=False)

disp = pd.read_csv("dev/disp_loaded.csv", sep=";")
disp.to_csv("dev/disp_clean.csv", index=False)

district = pd.read_csv("dev/district_loaded.csv", sep=";")
district.drop(['name','region'], axis=1, inplace=True)
print("Removing 'name' and 'region' columns from district data")
district.to_csv("dev/district_clean.csv", index=False)

loan = pd.read_csv("dev/loan_loaded.csv", sep=";")
loan.to_csv("dev/loan_clean.csv", index=False)

trans = pd.read_csv("dev/trans_loaded.csv", sep=";")
trans.to_csv("dev/trans_clean.csv", index=False)