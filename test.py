import pandas as pd
# import openpyxl
# import sys
# print(sys.executable)

all_sheets = pd.read_excel('Running Dinner dataset 2022.xlsx',sheet_name=None)
for sheet_name, sheet_df in all_sheets.items():
    print(f"sheet_name {sheet_name} data：")
    print(sheet_df)
