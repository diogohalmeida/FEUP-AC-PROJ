import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt


print("::::CLEANING::::")

account = pd.read_csv("dev/account_loaded.csv")
account.to_csv("dev/account_clean.csv", index=False)

card = pd.read_csv("dev/card_loaded.csv")
card.to_csv("dev/card_clean.csv", index=False)

client = pd.read_csv("dev/client_loaded.csv")
client.to_csv("dev/client_clean.csv", index=False)

disp = pd.read_csv("dev/disp_loaded.csv")
disp.to_csv("dev/disp_clean.csv", index=False)

district = pd.read_csv("dev/district_loaded.csv")
district.drop(['name','region'], axis=1, inplace=True)
print("Removing 'name' and 'region' columns from district data")

# Dealing with missing values in district
test = district.loc[district["unemploymant rate '95 "] != '?']
test["unemploymant rate '95 "] = [float(x) for x in test["unemploymant rate '95 "]]

mean_rate = test["unemploymant rate '95 "].mean()

district["unemploymant rate '95 "] = [mean_rate if x == "?" else float(x) for x in district["unemploymant rate '95 "]]
print("Replacing missing value in 'unemploymant rate '95 ' with mean of column and converting the whole column to float")

mean_no = test_2["no. of commited crimes '95 "].mean()

districts["no. of commited crimes '95 "] = [mean_no if x == "?" else float(x) for x in districts["no. of commited crimes '95 "]]

test_2 = district.loc[district["no. of commited crimes '95 "] != '?']
test_2["no. of commited crimes '95 "] = [float(x) for x in test["no. of commited crimes '95 "]]

district.to_csv("dev/district_clean.csv", index=False)

loan = pd.read_csv("dev/loan_loaded.csv")
loan.to_csv("dev/loan_clean.csv", index=False)

trans = pd.read_csv("dev/trans_loaded.csv")
trans["type"] = [i if i != "withdrawal in cash" else "withdrawal" for i in trans["type"]]
print("Renaming rows where type='withdrawal in cash' to 'withdrawal'")
trans["k_symbol"] = ["" if type(i) != str or i == " " else i for i in trans["k_symbol"]]
print("Renaming rows where k_symbol is null/NaN to ''")
trans["operation"] = ["" if type(i) == float else i for i in trans["operation"]]
print("Renaming rows where operation is null/NaN to ''")
trans.to_csv("dev/trans_clean.csv", index=False)