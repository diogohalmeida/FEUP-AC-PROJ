import pandas as pd
from processing import process
from datetime import date

submission_df = process()
today = date.today()

submission_df.to_csv(f"submissions/{str(today)}.csv", index=False)
