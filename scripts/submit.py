import pandas as pd
from datetime import date

submission_df = pd.read_csv("dev/modeled.csv")
today = date.today()

submission_df.to_csv(f"submissions/{str(today)}.csv", index=False)
