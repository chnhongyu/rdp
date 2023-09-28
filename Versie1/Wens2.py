import pandas as pd
B = 0 
Filepath_Dataset = 'Running Dinner dataset 2022.xlsx'
Kookte = pd.read_excel(Filepath_Dataset, sheet_name = 'Kookte vorig jaar', header = 1)

for gang in Kookte['Gang']:
    print(gang)