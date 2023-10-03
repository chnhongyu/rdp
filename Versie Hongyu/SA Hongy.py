import pandas as pd
import numpy as np
import random
import math
from Main import Constraints
from Main import Wensen

# Definieer een functie om de kost te berekenen die je wilt minimaliseren

    # In dit voorbeeld berekenen we de kost als het aantal unieke waarden in de geselecteerde kolommen

# Implementeer simulated annealing
def simulated_annealing(Filepath_Dataset, Filepath_Oplossing, temperatuur=1000, cool_rate=0.999, iteraties=3000):
       
    kolommen = ['Voor', 'Hoofd', 'Na']
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

        # Kies willekeurig twee verschillende rijen
        rij_indices = random.sample(range(len(Oplossing)), 2)
        
        # Selecteer willekeurig de kolom waarin je de waarden wilt omwisselen
        kolom = random.choice(kolommen)

        # Haal de waarden op uit de geselecteerde cellen
        waarde1 = Oplossing.at[rij_indices[0], kolom]
        waarde2 = Oplossing.at[rij_indices[1], kolom]

        # Maak een kopie van het DataFrame
        nieuw_df = Oplossing.copy()

        # Wissel de waarden in de geselecteerde kolom voor de geselecteerde cellen om
        nieuw_df.at[rij_indices[0], kolom] = waarde2
        nieuw_df.at[rij_indices[1], kolom] = waarde1
        
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
beste_oplossing, beste_kost = simulated_annealing('Running Dinner dataset 2023 v2.xlsx', 'Running Dinner eerste oplossing 2023 v2.xlsx')

# Print de beste oplossing en kost
print("Beste oplossing:")
print(beste_oplossing)
print("Beste kost:", beste_kost)