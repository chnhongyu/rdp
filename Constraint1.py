#------------------------------
# Constraint 1 zorgt voor dat elke deelnemer, elke gang, op 1 adres eet.
# dus deelnemer1: | a1 | a2 | a3 |
# input: Oplossing2021
# output: voldoet wel/niet aan constraint1

def constraint1(Oplossing):
    ### Oplossing is de dataframe van dat jaar. bijv Oplossing = pd.read_excel('.xlsx')###
    #functie checkt of de data voldoet aan constraint1, als statement True is voldoet het. False voldoet dus niet.
    statement = True

    Deelnemer_ongelijk_aan_3 = {}
    for deelnemer in Oplossing['Bewoner']:
        gangen = Oplossing[Oplossing['Bewoner']==deelnemer][['Voor','Hoofd','Na']].values[0]
        aantal_gangen = len(set(gangen))
        if aantal_gangen !=3:
            Deelnemer_ongelijk_aan_3[deelnemer]= aantal_gangen
    if len(Deelnemer_ongelijk_aan_3) >0:
        statement = False
    return print(statement)
