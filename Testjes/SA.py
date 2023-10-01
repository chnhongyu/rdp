import pandas as pd
import numpy as np
import random
import math

df = pd.read_excel('Running Dinner eerste oplossing 2021.xlsx')
# Kies de kolommen waarop je simulated annealing wilt toepassen
kolommen = ['Voor', 'Hoofd', 'Na']

# Definieer een functie om de kost te berekenen die je wilt minimaliseren
def bereken_kost(df):
    # Hier kun je je eigen kostfunctie implementeren
    # In dit voorbeeld berekenen we de kost als het aantal unieke waarden in de geselecteerde kolommen
    geselecteerde_waarden = df[kolommen].values.flatten()
    kost = len(set(geselecteerde_waarden))
    return kost

# Implementeer simulated annealing
def simulated_annealing(df, kolommen, temperatuur=100, cool_rate=0.99, iteraties=1000):
    huidige_kost = bereken_kost(df)
    beste_kost = huidige_kost
    beste_oplossing = df.copy()
    
    for i in range(iteraties):
        # Kies een willekeurige kolom om te wijzigen
        geselecteerde_kolom = random.choice(kolommen)
        
        # Kies willekeurig twee waarden uit de geselecteerde kolom om te verwisselen
        waarden = df[geselecteerde_kolom].unique()
        waarde1, waarde2 = random.sample(waarden, 2)
        
        # Maak een kopie van het DataFrame en wissel de waarden in de geselecteerde kolom
        nieuw_df = df.copy()
        nieuw_df.loc[nieuw_df[geselecteerde_kolom] == waarde1, geselecteerde_kolom] = waarde2
        nieuw_df.loc[nieuw_df[geselecteerde_kolom] == waarde2, geselecteerde_kolom] = waarde1
        
        # Bereken de kost van de nieuwe oplossing
        nieuwe_kost = bereken_kost(nieuw_df)
        
        # Bereken de kans om de nieuwe oplossing te accepteren
        kans = math.exp((huidige_kost - nieuwe_kost) / temperatuur)
        
        # Accepteer de nieuwe oplossing met een bepaalde kans
        if nieuwe_kost < huidige_kost or random.random() < kans:
            df = nieuw_df
            huidige_kost = nieuwe_kost
        
        # Update de beste oplossing indien nodig
        if nieuwe_kost < beste_kost:
            beste_kost = nieuwe_kost
            beste_oplossing = nieuw_df.copy()
        
        # Koel de temperatuur af
        temperatuur *= cool_rate
    
    return beste_oplossing, beste_kost

# Voer simulated annealing uit
beste_oplossing, beste_kost = simulated_annealing(df, kolommen)

# Print de beste oplossing en kost
print("Beste oplossing:")
print(beste_oplossing)
print("Beste kost:", beste_kost)