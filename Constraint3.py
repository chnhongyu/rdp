import pandas as pd 

Oplossing2021Excel = 'Running Dinner eerste oplossing 2021.xlsx'
Oplossing2021 = pd.read_excel(Oplossing2021Excel)

Dataset2021Excel = 'Running Dinner dataset 2021.xlsx'
Bewoners2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Bewoners')
Adressen2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Adressen')
Paar2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Paar blijft bij elkaar', header = 1)
Buren2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Buren', header = 1)
Kookte2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Kookte vorig jaar', header = 1)
Tafelgenoot2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Tafelgenoot vorig jaar', header = 1)

#-----------------------------
# Oplossing2022Excel = 'Running Dinner eerste oplossing 2022.xlsx'
# Oplossing2022 = pd.read_excel(Oplossing2022Excel)

# Dataset2022Excel = 'Running Dinner dataset 2022.xlsx'
# Bewoners2022 = pd.read_excel(Dataset2022Excel, sheet_name = 'Bewoners')
# Adressen2022 = pd.read_excel(Dataset2021Excel, sheet_name = 'Adressen')
# Paar2022 = pd.read_excel(Dataset2022Excel, sheet_name = 'Paar blijft bij elkaar', header = 1)
# Buren2022 = pd.read_excel(Dataset2022Excel, sheet_name = 'Buren', header = 1)
# Kookte2022 = pd.read_excel(Dataset2022Excel, sheet_name = 'Kookte vorig jaar', header = 1)
# Tafelgenoot2022 = pd.read_excel(Dataset2022Excel, sheet_name = 'Tafelgenoot vorig jaar', header = 1)

#------------------------------
# Constraint 3 zorgt voor alle adres