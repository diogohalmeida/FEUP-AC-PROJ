import pandas as pd

print("::::LOADING::::")

account = pd.read_csv("dataset/account.csv", sep=";")
account.rename(columns={"date": "date_account"}, inplace=True)
print("Loading account.csv renaming ['date'] to ['date_account']")
account.to_csv("dev/account_loaded.csv", index=False)

card = pd.read_csv("dataset/card_train.csv", sep=";")
card.rename(columns={"type": "type_card", "issued": "date_card"}, inplace=True)
print("Loading card_train.csv renaming ['type', 'issued'] to ['type_card', 'date_card']")
card.to_csv("dev/card_loaded.csv", index=False)

client = pd.read_csv("dataset/client.csv", sep=";")
print("Loading client.csv")
client.to_csv("dev/client_loaded.csv", index=False)

disp = pd.read_csv("dataset/disp.csv", sep=";")
disp.rename(columns={"type": "type_disp"})
print("Loading disp.csv renaming ['type'] to ['type_disp']")
disp.to_csv("dev/disp_loaded.csv", index=False)

district = pd.read_csv("dataset/district.csv", sep=";")
district.rename(columns={"code ": "district_id", "name ": "name"}, inplace=True)
print("Loading district.csv renaming ['code ', 'name '] to ['district_id', 'name']")
district.to_csv("dev/district_loaded.csv", index=False)

loan = pd.read_csv("dataset/loan_train.csv", sep=";")
loan.rename(columns={"date": "date_loan", "amount": "amount_loan"})
print("Loading loan_train.csv renaming ['date', 'amount'] to ['date_loan', 'amount_loan']")
loan.to_csv("dev/loan_loaded.csv", index=False)

trans = pd.read_csv("dataset/trans_train.csv", sep=";")
trans.rename(columns={"date": "date_trans", "type": "type_trans", "amount": "amount_trans"})
print("Loading trans_train.csv renaming ['date', 'type', 'amount'] to ['date_trans', 'type_trans', 'amount_trans']")
trans.to_csv("dev/trans_loaded.csv", index=False)