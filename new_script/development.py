# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 11:11:37 2021

@author: diogo
"""

import pandas
from collections import Counter
import numpy as np
import math


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


loan_year= []

std_balances = []
min_balances = []
max_balances = []
mean_balances = []
recent_balances = []

total_credit_list = []
min_credits = []
max_credits = []
mean_credits = []
std_credits = []
total_credit_times_list = []

total_withdrawal_list = []
min_withdrawals = []
max_withdrawals = []
mean_withdrawals = []
std_withdrawals = []
total_withdrawal_times_list = []

owner_ages_at_loan = []
owner_ages_at_account_creation = []

account_has_disponent_list = []

has_junior_card_list = []
has_classic_card_list = []
has_gold_card_list = []

#k_symbol
has_interest_credit_list = []
has_payment_for_statement_list = []
has_household_list = []
has_old_age_pension_list = []
has_insurrance_payment_list = []
has_sanction_if_negative_list = []

#operation types
credits_in_cash_list = []
collections_from_bank_list = []
withdrawals_in_cash_list = []
remittances_to_bank_list =[]
credit_card_withdrawals_list = []

months_until_bankrupt_list = []
months_until_bankrupt_loan_duration_diff_list = []
for account_id in loan_train["account_id"]:
    #TRANSACTION BALANCES CALC
    loan_row = loan_train.loc[loan_train['account_id'] == account_id]
    full_data_rows = disp_client_account_district_card_trans.loc[disp_client_account_district_card_trans['account_id'] == account_id]
    balance_list = full_data_rows["balance"].tolist()
    min_balance = min(balance_list)
    max_balance = max(balance_list)
    mean_balance = sum(balance_list)/len(balance_list)
    std_balance = np.array(balance_list).std()
    
    trans_date_list = full_data_rows["date_trans"].tolist()
    loan_date = loan_row["date_loan"].tolist()[0]
    
    nearest_trans_date = nearest(trans_date_list, loan_date)
    balance_at_loan_list = full_data_rows.loc[full_data_rows['date_trans'] == nearest_trans_date]["balance"].tolist()
    
    recent_balance = sum(balance_at_loan_list)/len(balance_at_loan_list)
    
    min_balances.append(min_balance)
    max_balances.append(max_balance)
    mean_balances.append(mean_balance)
    std_balances.append(std_balance)
    recent_balances.append(recent_balance)
    
    
    #TOTAL CREDIT/WITHDRAWAL
    #TOTAL TIMES CREDIT/WITHDRAW
    #MAX, MIN, MEAN AND STD CREDIT/WITHDRAWAL
    credit_list = full_data_rows.loc[full_data_rows['type_trans'] == "credit"]["amount"].tolist()
    total_credit = sum(credit_list)
    total_credit_times = len(credit_list)
    if total_credit_times != 0:
        min_credit = min(credit_list)
        max_credit = max(credit_list)
        mean_credit = sum(credit_list)/len(credit_list)
        std_credit = np.array(credit_list).std()
    else:
        min_credit = 0
        max_credit = 0
        mean_credit = 0
        std_credit = 0
    total_credit_list.append(total_credit)
    total_credit_times_list.append(total_credit_times)
    min_credits.append(min_credit)
    max_credits.append(max_credit)
    mean_credits.append(mean_credit)
    std_credits.append(std_credit)
    
    withdrawal_list = full_data_rows.loc[full_data_rows['type_trans'] == "withdrawal"]["amount"].tolist()
    total_withdrawal = sum(withdrawal_list)
    total_withdrawal_times = len(withdrawal_list)
    if total_withdrawal_times != 0:
        min_withdrawal = min(withdrawal_list)
        max_withdrawal = max(withdrawal_list)
        mean_withdrawal= sum(withdrawal_list)/len(withdrawal_list)
        std_withdrawal = np.array(withdrawal_list).std()
    else:
        min_withdrawal = 0
        max_withdrawal = 0
        mean_withdrawal = 0
        std_withdrawal = 0
    total_withdrawal_list.append(total_withdrawal)
    total_withdrawal_times_list.append(total_withdrawal_times)
    min_withdrawals.append(min_withdrawal)
    max_withdrawals.append(max_withdrawal)
    mean_withdrawals.append(mean_withdrawal)
    std_withdrawals.append(std_withdrawal)
    
    
    
    #OWNER AGE AT LOAN CALC
    loan_year.append(loan_row["date_loan"].tolist()[0].year)
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
    
    
    
    #REGISTER ACCOUNT K_SYMBOLS
    k_symbols = full_data_rows["k_symbol"].tolist()
    has_interest_credit = Counter(k_symbols)['interest credited']
    has_payment_for_statement = Counter(k_symbols)['payment for statement']
    has_household = Counter(k_symbols)['household']
    has_old_age_pension = Counter(k_symbols)['old-age pension']
    has_insurrance_payment = Counter(k_symbols)['insurrance payment']
    has_sanction_if_negative = Counter(k_symbols)['sanction interest if negative balance']
        
    has_interest_credit_list.append(has_interest_credit)
    has_payment_for_statement_list.append(has_payment_for_statement)
    has_household_list.append(has_household)
    has_old_age_pension_list.append(has_old_age_pension)
    has_insurrance_payment_list.append(has_insurrance_payment)
    has_sanction_if_negative_list.append(has_sanction_if_negative)
    
    
    #OPERATIONS LIST
    operations = full_data_rows["operation"].tolist()
    
    credits_in_cash = Counter(operations)['credit in cash']
    collections_from_bank = Counter(operations)['collection from another bank']
    withdrawals_in_cash = Counter(operations)['withdrawal in cash']
    remittances_to_bank = Counter(operations)['remittance to another bank']
    credit_card_withdrawals = Counter(operations)['credit card withdrawal']

    credits_in_cash_list.append(credits_in_cash)
    collections_from_bank_list.append(collections_from_bank)
    withdrawals_in_cash_list.append(withdrawals_in_cash)
    remittances_to_bank_list.append(remittances_to_bank)
    credit_card_withdrawals_list.append(credit_card_withdrawals)
    
    
    #MONTHS UNTIL BANKRUPT
    months_until_bankrupt = math.floor(recent_balance/loan_row["payments"].tolist()[0])
    months_until_bankrupt_list.append(months_until_bankrupt)
    
    #MONTHS UNTIL BANKRUPT AND LOAN DURATION DIFF
    months_until_bankrupt_loan_duration_diff_list.append(months_until_bankrupt-loan_row["duration"].tolist()[0])

#START MERGING
#DROP LOAN DATE(WILL HAVE OWNER AGE AT LOAN INSTEAD)
loan_clean = loan_train.drop(columns=["date_loan"])


loan_clean["loan_year"] = loan_year
loan_clean["owner_age_at_loan"] = owner_ages_at_loan
loan_clean["owner_age_at_account_creation"] = owner_ages_at_account_creation
loan_clean["has_disponent"] = account_has_disponent_list
loan_clean["has_junior_card"] = has_junior_card_list
loan_clean["has_classic_card"] = has_classic_card_list
loan_clean["has_gold_card"] = has_gold_card_list

loan_clean["min_balance"] = min_balances
loan_clean["max_balance"] = max_balances
loan_clean["mean_balance"] = mean_balances
loan_clean["std_balance"] = std_balances
loan_clean["recent_balance"] = recent_balances

loan_clean["total_credit"] = total_credit_list
loan_clean["min_credit"] = min_credits
loan_clean["max_credit"] = max_credits
loan_clean["mean_credit"] = mean_credits
loan_clean["std_credit"] = std_credits
loan_clean["total_withdrawal"] = total_withdrawal_list
loan_clean["min_withdrawal"] = min_withdrawals
loan_clean["max_withdrawal"] = max_withdrawals
loan_clean["mean_withdrawal"] = mean_withdrawals
loan_clean["std_withdrawal"] = std_withdrawals
loan_clean["total_credit_times"] = total_credit_times_list
loan_clean["total_withdrawal_times"] = total_withdrawal_times_list

loan_clean["interest_credit"] = has_interest_credit_list
loan_clean["payment_for_statement"] = has_payment_for_statement_list
loan_clean["household"] = has_household_list
loan_clean["old-age_pension"] = has_old_age_pension_list
loan_clean["insurrance_payment"] = has_insurrance_payment_list
loan_clean["sanction_interest_if_negative_balance"] = has_sanction_if_negative_list

loan_clean["credit_in_cash"] = credits_in_cash_list
loan_clean["collection_from_another_bank"] = collections_from_bank_list
loan_clean["withdrawal_in_cash"] = withdrawals_in_cash_list
loan_clean["remittance_to_another_bank"] = remittances_to_bank_list
loan_clean["credit_card_withdrawal"] = credit_card_withdrawals_list

loan_clean["months_until_bankrupt"] = months_until_bankrupt_list
loan_clean["months_until_bankrupt_loan_duration_diff"] = months_until_bankrupt_loan_duration_diff_list

#MERGE WITH THE REST OF DATA
loan_clean = pandas.merge(loan_clean, disp_client_account_district.loc[disp_client_account_district['type_disp'] == "OWNER"], on="account_id", how="inner")


#DROP ACCOUNT DATE(WILL HAVE OWNER AGE AT ACCOUNT CREATION INSTEAD)
loan_clean = loan_clean.drop(columns=["date_account"])
loan_clean = loan_clean.drop(columns=["birthdate"])
    

#DROP TYPE DISP (ALL OWNERS SO ITS USELESS)
loan_clean = loan_clean.drop(columns=["type_disp"])

#DROP IDS
loan_clean = loan_clean.drop(columns=["loan_id","account_id","disp_id","client_id","district_id"])

#WRITE TO CSV
loan_clean.to_csv("loans_train.csv", sep=",", index=False)       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        