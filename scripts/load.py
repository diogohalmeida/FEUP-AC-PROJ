import pandas as pd

print("::::LOADING::::")

account = pd.read_csv("dataset/account.csv", sep=";")
print("Loading account.csv")
account.to_csv("dev/account_loaded.csv", index=False)

card = pd.read_csv("dataset/card_train.csv", sep=";")
print("Loading card_train.csv")
card.to_csv("dev/card_loaded.csv", index=False)

client = pd.read_csv("dataset/client.csv", sep=";")
print("Loading client.csv")
client.to_csv("dev/client_loaded.csv", index=False)

disp = pd.read_csv("dataset/disp.csv", sep=";")
print("Loading disp.csv")
disp.to_csv("dev/disp_loaded.csv", index=False)

district = pd.read_csv("dataset/district.csv", sep=";")
district.rename(columns={"code ": "district_id", "name ": "name"}, inplace=True)
print("Loading district.csv renaming ['code ', 'name '] to ['district_id', 'name']")
district.to_csv("dev/district_loaded.csv", index=False)

loan = pd.read_csv("dataset/loan_train.csv", sep=";")
print("Loading loan_train.csv")
loan.to_csv("dev/loan_loaded.csv", index=False)

trans = pd.read_csv("dataset/trans_train.csv", sep=";")
print("Loading trans_train.csv")
trans.to_csv("dev/trans_loaded.csv", index=False)