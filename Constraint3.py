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

#------------------------------
# Constraint 3 zorgt voor als je gang g op adres a kookt, ook op adres a gang g eet
# eerst alle adressen die niet hoef te koken laten droppen
# vervolgens loop over elk bewoner, de constraint checken
# een lijst maken voor de bewoners die niet aan de constraints voldoet
# als de lijst leeg is, dan voldoet de data aan de constraint
#------------------------------
# input: Oplossing2021
# huisadres voor elke deelnemer, moet onder de gang staan wat ze gaan koken
# output: Voldoet wel/niet aan de constraint

def constraint3(oplossing):
    Checklijst = []
    df_kokend = oplossing.dropna(subset=['kookt'])
    for deelnemer in range(len(df_kokend)):
        gang = df_kokend.iloc[deelnemer]['kookt']
        lhs = df_kokend.iloc[deelnemer][gang]
        rhs = df_kokend.iloc[deelnemer]['Huisadres']
        if lhs != rhs:
            Checklijst.append(df_kokend.iloc[deelnemer]['Bewoner'])
    statement = len(Checklijst) == 0
    if statement:
        print('Constraint 3 is voldaan')
    return statement


constraint3(Oplossing2021)
