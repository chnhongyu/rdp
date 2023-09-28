import pandas as pd

Filepath_Dataset = 'Running Dinner dataset 2022.xlsx'
Filepath_Oplossing = 'Running Dinner eerste oplossing 2022.xlsx'
Kookte = pd.read_excel(Filepath_Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
Oplossing = pd.read_excel(Filepath_Oplossing)

import pandas as pd

# Stel dat Oplossing en Kookte DataFrames zijn
# Merge de twee DataFrames op basis van 'Huisadres' en 'Gang'
merged_df = Oplossing.merge(Kookte, left_on=['Huisadres', 'kookt'], right_on=['Huisadres', 'Gang'], how='inner')
per_huisadressen = merged_df['Huisadres'].nunique()

# Het aantal overeenkomstige rijen is de lengte van de samengevoegde DataFrame
# B = len(per_huisadressen)


    