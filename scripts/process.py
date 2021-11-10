import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

print("::::PROCESSING::::")

# Loading
merged = pd.read_csv("dev/merged.csv")

# Dates and gender
dates = merged["birth_number"]
dates = [str(date)[:2] + "-" + str(date)[2:4] + "-" + str(date)[4:] for date in dates]

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
    new_dates.append(date[0:2] + "-" + month + "-" + date[6:8])
    sex.append(gender)
    
ages = []
for date in new_dates:
    year = int("19" + date[0:2])
    age = 2021 - year
    ages.append(age)
    
merged = merged.drop(["birth_number"], axis=1)
merged = merged.assign(sex = sex, age = ages)
print("Replacing 'birth_number' column with 'sex' and 'age' columns")

# Dropping ids
merged = merged.drop(["client_id", "district_id", "trans_id", "disp_id", "card_id", "account_id", "loan_id"], axis=1)
print("Dropping 'client_id', 'district_id', 'trans_id', 'disp_id', 'card_id', 'account_id', 'loan_id'")

# Removing related columns
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

# Create correlation matrix
corr_matrix = merged.corr().abs()
plt.figure(figsize = (20,6))
sb.heatmap(corr_matrix,annot=True)

# Select upper triangle of correlation matrix
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

# Find features with correlation greater than 0.95
to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]

# Drop features 
merged.drop(to_drop, axis=1, inplace=True)

print("{} Dropped columns: {} due to correlation > 0.95".format(len(to_drop), to_drop) )

# Removing rows with nan values for status
merged.dropna(subset=["status"], inplace=True)
print("Removing rows with nan values for 'status'")

# Saving final result to csv
merged.to_csv("dev/processed.csv", index=False)