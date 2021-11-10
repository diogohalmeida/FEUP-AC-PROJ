import pandas as pd

print("::::MERGING::::")

account = pd.read_csv("dev/account_clean.csv")

card = pd.read_csv("dev/card_clean.csv")

client = pd.read_csv("dev/client_clean.csv")

disp = pd.read_csv("dev/disp_clean.csv")

district = pd.read_csv("dev/district_clean.csv")

loan = pd.read_csv("dev/loan_clean.csv")

trans = pd.read_csv("dev/trans_clean.csv")


client_disp = pd.merge(client, disp, on="client_id")
print("Merging client and disp (on='client_id') into client_disp")

client_disp.rename(columns={"type": "type_disp"}, inplace=True)
print("Renaming 'type' to 'type_disp' in client_disp")

card.rename(columns={"type": "type_card"}, inplace=True)
print("Renaming 'type' to 'type_card in card")

client_disp_card = pd.merge(client_disp, card, on="disp_id", how="outer")
print("Merging client_disp and card (on='disp_id',how='outer') into client_disp_card")

client_disp_card_district = pd.merge(client_disp_card, district, on="district_id")
print("Merging client_disp_card and district (on='district_id') into client_disp_card_district")

client_disp_card_district_account = pd.merge(client_disp_card_district, account, on="account_id")
print("Merging client_disp_card_district and account (on='account_id') into client_disp_card_district_account")

client_disp_card_district_account_trans = pd.merge(client_disp_card_district_account, trans, on="account_id")
print("Merging client_disp_card_district_account and trans (on='account_id') into client_disp_card_district_account_trans")

merged = pd.merge(client_disp_card_district_account_trans, loan, on="account_id", how="outer")
print("Merging client_disp_card_district_account_trans and loan (on='account_id',how='outer') into merged")

merged.to_csv("dev/merged.csv", index=False)