import pandas as pd 
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
