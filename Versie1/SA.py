import pandas as pd
import numpy as np
import random
import math
from Main import Constraints
from Main import Wensen

# Kies de kolommen waarop je simulated annealing wilt toepassen
kolommen = ['Voor', 'Hoofd', 'Na']

# Definieer een functie om de kost te berekenen die je wilt minimaliseren

    # In dit voorbeeld berekenen we de kost als het aantal unieke waarden in de geselecteerde kolommen

# Implementeer simulated annealing
def simulated_annealing(Filepath_Dataset, Filepath_Oplossing, kolommen, temperatuur=100, cool_rate=0.99, iteraties=500):
       
    Oplossing = pd.read_excel(Filepath_Oplossing)
    
    Bewoners = pd.read_excel(Filepath_Dataset, sheet_name = 'Bewoners')
    Adressen = pd.read_excel(Filepath_Dataset, sheet_name = 'Adressen')
    Paar = pd.read_excel(Filepath_Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
    Buren = pd.read_excel(Filepath_Dataset, sheet_name = 'Buren', header = 1)
    Kookte = pd.read_excel(Filepath_Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
    Tafelgenoot = pd.read_excel(Filepath_Dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1) 
    
    huidige_kost = Wensen(Oplossing, Kookte, Adressen, Buren, Tafelgenoot) 
    beste_kost = huidige_kost
    beste_oplossing = Oplossing.copy()
    
    for i in range(iteraties):
        # Kies een willekeurige kolom om te wijzigen
        geselecteerde_kolom = random.choice(kolommen)
        
        # Kies willekeurig twee waarden uit de geselecteerde kolom om te verwisselen
        waarden = Oplossing[geselecteerde_kolom].unique()
        waarden_lijst = waarden.tolist()
        waarde1, waarde2 = random.sample(waarden_lijst, 2)
        
        # Maak een kopie van het DataFrame en wissel de waarden in de geselecteerde kolom
        nieuw_df = Oplossing.copy()
        nieuw_df.loc[nieuw_df[geselecteerde_kolom] == waarde1, geselecteerde_kolom] = waarde2
        nieuw_df.loc[nieuw_df[geselecteerde_kolom] == waarde2, geselecteerde_kolom] = waarde1
        
        # Bereken de kost van de nieuwe oplossing
        nieuwe_kost = Wensen(nieuw_df, Kookte, Adressen, Buren, Tafelgenoot)
        
        # Bereken de kans om de nieuwe oplossing te accepteren
        kans = math.exp((huidige_kost - nieuwe_kost) / temperatuur)
        
        # Accepteer de nieuwe oplossing met een bepaalde kans
        if nieuwe_kost < huidige_kost or random.random() < kans:
            Oplossing = nieuw_df
            huidige_kost = nieuwe_kost
        
        # Update de beste oplossing indien nodig
        if nieuwe_kost < beste_kost:
            beste_kost = nieuwe_kost
            beste_oplossing = nieuw_df.copy()
        
        # Koel de temperatuur af
        temperatuur *= cool_rate
    
    return beste_oplossing, beste_kost

# Voer simulated annealing uit
beste_oplossing, beste_kost = simulated_annealing('Running Dinner dataset 2023 v2.xlsx', 'Running Dinner eerste oplossing 2023 v2.xlsx', kolommen)

# Print de beste oplossing en kost
print("Beste oplossing:")
print(beste_oplossing)
print("Beste kost:", beste_kost)