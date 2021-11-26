# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 11:11:37 2021

@author: diogo
"""

import pandas
from collections import Counter
import numpy as np


disp = pandas.read_csv("dataset/disp.csv", sep=";")

client = pandas.read_csv("dataset/client.csv", sep=";")

account= pandas.read_csv("dataset/account.csv", sep=";")

district = pandas.read_csv("dataset/district.csv", sep=";")

card_train = pandas.read_csv("dataset/card_train.csv", sep=";")
card_test = pandas.read_csv("dataset/card_test.csv", sep=";")

trans_train = pandas.read_csv("dataset/trans_train.csv", sep=";")
trans_test = pandas.read_csv("dataset/trans_test.csv", sep=";")

loan_train = pandas.read_csv("dataset/loan_train.csv", sep=";")
loan_test = pandas.read_csv("dataset/loan_test.csv", sep=";")


#FIX DISTRICT MISSING VALUES
district["unemploymant rate 1995 "] = np.where(district["unemploymant rate 1995 "] == '?', district["unemploymant rate 1996 "], district["unemploymant rate 1995 "])
district["unemploymant rate 1995 "] = pandas.to_numeric(district["unemploymant rate 1995 "])


#REPLACE MISSING VALUES WITH NEXT COLUMN'S VALUES
district["no. of commited crimes 1995 "] = np.where(district["no. of commited crimes 1995 "] == '?', district["no. of commited crimes 1996 "], district["no. of commited crimes 1995 "])
district["no. of commited crimes 1995 "] = pandas.to_numeric(district["no. of commited crimes 1995 "])



#JOIN CARD AND TRANS TRAIN AND TEST SETS
full_card = pandas.concat([card_train, card_test])
# dups = full_card.pivot_table(columns=['card_id'], aggfunc='size')
# print (dups)

full_trans = pandas.concat([trans_train, trans_test])
# dups_color = full_trans.pivot_table(columns=['trans_id'], aggfunc='size')
# print (dups)


#FIX DIST





#FIX DATES
def parse_dates(date):
    year = "19" + str(date[:2])
    month = str(date[2:4])
    day = str(date[4:])
    return year + "/" + month  + "/" + day

account = account.rename(columns={"date": "date_account"})
account["date_account"] = account["date_account"].map(lambda x: parse_dates(str(x)))
account["date_account"] = pandas.to_datetime(account["date_account"], format = "%Y/%m/%d")

full_card = full_card.rename(columns={"issued": "date_card"})
full_card["date_card"] = full_card["date_card"].map(lambda x: parse_dates(str(x)))
full_card["date_card"] = pandas.to_datetime(full_card["date_card"], format = "%Y/%m/%d")

loan_train = loan_train.rename(columns={"date": "date_loan"})
loan_train["date_loan"] = loan_train["date_loan"].map(lambda x: parse_dates(str(x)))
loan_train["date_loan"] = pandas.to_datetime(loan_train["date_loan"], format = "%Y/%m/%d")

loan_test = loan_test.rename(columns={"date": "date_loan"})
loan_test["date_loan"] = loan_test["date_loan"].map(lambda x: parse_dates(str(x)))
loan_test["date_loan"] = pandas.to_datetime(loan_test["date_loan"], format = "%Y/%m/%d")

full_trans = full_trans.rename(columns={"date": "date_trans"})
full_trans["date_trans"] = full_trans["date_trans"].map(lambda x: parse_dates(str(x)))
full_trans["date_trans"] = pandas.to_datetime(full_trans["date_trans"], format = "%Y/%m/%d")

#FIX BIRTH DATES AND GENDERS IN CLIENT DATASET
def handle_dates(dates):
    new_dates = []
    sex = []
    for date in dates:
        month = int(date[3:5])
        gender = ""
        if month > 12:
            month = month - 50
            gender = "female"
        else:
            gender = "male"
        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)
        new_dates.append("19" + date[0:2] + "/" + month + "/" + date[6:8])
        sex.append(gender)
    return (new_dates, sex)

dates = client["birth_number"]

dates = [str(date)[:2] + "/" + str(date)[2:4] + "/" + str(date)[4:] for date in dates]

dates, sex = handle_dates(dates)

client = client.drop(["birth_number"], axis=1)

client = client.assign(sex = sex, birthdate = dates)

client["birthdate"] = pandas.to_datetime(client["birthdate"], format = "%Y/%m/%d")

#DROP USELESS COLUMNS FROM DISTRICT: NAME AND REGION 
district_clean = district.rename(columns={"code ": "district_id"})
district_clean = district_clean.drop(columns = ['name ','region'])

#DROP USELESS DISTRICT ID COLUMN FROM ACCOUNT (ALREADY IN CLIENT)
account_clean = account.drop(columns = ['district_id'])

#RENAME TYPE DISP, TYPE CARD AND TYPE TRANS
full_card = full_card.rename(columns={"type": "type_card"})
disp_clean = disp.rename(columns={"type": "type_disp"})
full_trans = full_trans.rename(columns={"type": "type_trans"})

#DROP USELESS COLUMNS FROM FULL_TRANS
full_trans = full_trans.drop(columns = ['account'])


#DATASET JOIN
#CLIENT WITH DISP
disp_client = pandas.merge(client, disp_clean, on="client_id", how="inner")

#DISP_CLIENT WITH ACCOUNT
disp_client_account = pandas.merge(disp_client, account_clean, on="account_id", how="inner")

#DISP_CLIENT_ACCOUNT WITH DISTRICT
disp_client_account_district = pandas.merge(disp_client_account, district_clean, on="district_id", how="inner")

#DISP_CLIENT_ACCOUNT_DISTRICT_CARD
disp_client_account_district_card = pandas.merge(disp_client_account_district, full_card, on="disp_id", how="left")

#DISP_CLIENT_ACCOUNT_DISTRICT_CARD_TRANS
disp_client_account_district_card_trans = pandas.merge(disp_client_account_district_card, full_trans, on="account_id", how="inner")
# dups = disp_client_account_district_card_trans.pivot_table(columns=['trans_id'], aggfunc='size')
# print (dups)

"""
CREATE FINAL DATASET WITH: 
    - Max, min and average balance. Balance at date closest to loan.
    - If account has a Disponent (having an owner is already guaranteed)
    - Owner Age at Loan
    - If the client has a card, and what type
    - Owner Age at account creation
    - Total Credit / Total Withdrawal 
"""



def nearest(items, pivot):
    items_clean = [i for i in items if pivot >= i]
    return min(items_clean, key=lambda x: pivot - x)



min_balances = []
max_balances = []
mean_balances = []
recent_balances = []
total_credit_list = []
total_withdrawal_list = []
total_credit_times_list = []
total_withdrawal_times_list = []
owner_ages_at_loan = []
owner_ages_at_account_creation = []
account_has_disponent_list = []
has_junior_card_list = []
has_classic_card_list = []
has_gold_card_list = []
for account_id in loan_test["account_id"]:
    #TRANSACTION BALANCES CALC
    loan_row = loan_test.loc[loan_test['account_id'] == account_id]
    full_data_rows = disp_client_account_district_card_trans.loc[disp_client_account_district_card_trans['account_id'] == account_id]
    balance_list = full_data_rows["balance"].tolist()
    min_balance = min(balance_list)
    max_balance = max(balance_list)
    mean_balance = sum(balance_list)/len(balance_list)
    
    trans_date_list = full_data_rows["date_trans"].tolist()
    loan_date = loan_row["date_loan"].tolist()[0]
    
    nearest_trans_date = nearest(trans_date_list, loan_date)
    balance_at_loan_list = full_data_rows.loc[full_data_rows['date_trans'] == nearest_trans_date]["balance"].tolist()
    
    recent_balance = sum(balance_at_loan_list)/len(balance_at_loan_list)
    
    min_balances.append(min_balance)
    max_balances.append(max_balance)
    mean_balances.append(mean_balance)
    recent_balances.append(recent_balance)
    
    
    #TOTAL CREDIT/WITHDRAWAL
    #TOTAL TIMES CREDIT/WITHDRAW
    total_credit = sum(full_data_rows.loc[full_data_rows['type_trans'] == "credit"]["amount"].tolist())
    total_credit_times = len(full_data_rows.loc[full_data_rows['type_trans'] == "credit"]["amount"].tolist())
    total_credit_list.append(total_credit)
    total_credit_times_list.append(total_credit_times)
    total_withdrawal = sum(full_data_rows.loc[full_data_rows['type_trans'] == "withdrawal"]["amount"].tolist())
    total_withdrawal_times = len(full_data_rows.loc[full_data_rows['type_trans'] == "withdrawal"]["amount"].tolist())
    total_withdrawal_list.append(total_withdrawal)
    total_withdrawal_times_list.append(total_withdrawal_times)
    
    #OWNER AGE AT LOAN CALC
    owner_age_at_loan = (loan_row["date_loan"].tolist()[0] - (full_data_rows.loc[full_data_rows['type_disp'] == "OWNER"]["birthdate"].tolist()[0])).days//365
    owner_ages_at_loan.append(owner_age_at_loan)
    
    #OWNER AGE AT ACCOUNT CREATION CALC
    owner_age_at_account_creation = (full_data_rows.loc[full_data_rows['type_disp'] == "OWNER"]["date_account"].tolist()[0] - (full_data_rows.loc[full_data_rows['type_disp'] == "OWNER"]["birthdate"].tolist()[0])).days//365
    owner_ages_at_account_creation.append(owner_age_at_account_creation)
    
    #IF ACCOUNT HAS DISPONENT
    if full_data_rows.loc[full_data_rows['type_disp'] == "DISPONENT"].empty:
        account_has_disponent_list.append(0)
    else:
        account_has_disponent_list.append(1)
        
    #REGISTER IF CLIENT HAS 
    type_card = full_data_rows.loc[full_data_rows['type_disp'] == "OWNER"]["type_card"].tolist()[0]
    if isinstance(type_card, str):
        if type_card == "junior":
            has_junior_card = 1
            has_classic_card = 0 
            has_gold_card = 0 
        elif type_card == "classic":
            has_junior_card = 0
            has_classic_card = 1
            has_gold_card = 0 
        elif type_card == "gold":
            has_junior_card = 0
            has_classic_card = 0
            has_gold_card = 1
    else:   
        has_junior_card = 0 
        has_classic_card = 0 
        has_gold_card = 0 
        
    has_junior_card_list.append(has_junior_card)
    has_classic_card_list.append(has_classic_card)
    has_gold_card_list.append(has_gold_card)
    

#START MERGING
#DROP LOAN DATE(WILL HAVE OWNER AGE AT LOAN INSTEAD)
loan_clean = loan_test.drop(columns=["date_loan"])


loan_clean["owner_age_at_loan"] = owner_ages_at_loan
loan_clean["owner_age_at_account_creation"] = owner_ages_at_account_creation
loan_clean["has_disponent"] = account_has_disponent_list
loan_clean["has_junior_card"] = has_junior_card_list
loan_clean["has_classic_card"] = has_classic_card_list
loan_clean["has_gold_card"] = has_gold_card_list

loan_clean["min_balance"] = min_balances
loan_clean["max_balance"] = max_balances
loan_clean["mean_balance"] = mean_balances
loan_clean["recent_balance"] = recent_balances

loan_clean["total_credit"] = total_credit_list
loan_clean["total_withdrawal"] = total_withdrawal_list
loan_clean["total_credit_times"] = total_credit_times_list
loan_clean["total_withdrawal_times"] = total_withdrawal_times_list

#MERGE WITH THE REST OF DATA
loan_clean = pandas.merge(loan_clean, disp_client_account_district.loc[disp_client_account_district['type_disp'] == "OWNER"], on="account_id", how="inner")


#DROP ACCOUNT DATE(WILL HAVE OWNER AGE AT ACCOUNT CREATION INSTEAD)
loan_clean = loan_clean.drop(columns=["date_account"])
loan_clean = loan_clean.drop(columns=["birthdate"])
    

#DROP TYPE DISP (ALL OWNERS SO ITS USELESS)
loan_clean = loan_clean.drop(columns=["type_disp"])

#DROP IDS
loan_clean = loan_clean.drop(columns=["account_id","disp_id","client_id","district_id"])   


#DROP STATUS (FOR TEST ONLY)
loan_clean = loan_clean.drop(columns=["status"])


#WRITE TO CSV
loan_clean.to_csv("loans_test.csv", sep=",",  index=False)    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        