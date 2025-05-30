# -*- coding: utf-8 -*-
"""
Created on 10.02.2025

@author: tomaž dolinar
"""
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt




class Rezanje_konic:
    def __init__(self,consumption, production):   
        self.cons=consumption   #consumption (+) moč v kW       
        self.prod=production    #production (+) moč v kW


    def profil_rezanja_konic(self,SoC_max,SoC_min,bat_max,bat_min):

        cons=self.cons-self.prod #moč odjema kar čuti omrežje v 15 min intervalu
        cons.loc[cons == 0] = 1
        SoC=float(bat_max)
        SoC_b=float(bat_max)
        SoC_max = float(SoC_max)
        SoC_min = float(SoC_min)
        bat_max = float(bat_max)  # Ensure it's a single number
        bat_min = float(bat_min)
        bat_p=[]
        bat_soc=[]


        cons_dnevi = [cons[i:i + 96] for i in range(0, len(cons),96)]# zamenjaj 96 z len(cons)
        count_dnevi = 0
        #začetek for loopa
        for cons_dan in cons_dnevi:
            count_dnevi += 1
            srednja_vrednost = cons_dan.sum()/96
            max_vrednost = cons_dan.max()
            min_vrednost = cons_dan.min()
            maksimalna_meja_polnjenja = srednja_vrednost - min_vrednost
            minimalna_meja_praznjenja = max_vrednost - srednja_vrednost

            ##################################################################### DOLOČANJE padcev in vzponov v enem dnevu, morajo biti zaporedni
            padci = {"indeks": [], "dan": []}
            vzponi = {"indeks": [], "dan": []}  


            for x in range(len(cons_dan)):
                if (x  >= 0) and (x+1 < len(cons_dan)):
                    # padci
                    if cons_dan.iloc[x] > srednja_vrednost and cons_dan.iloc[x+1] < srednja_vrednost:
                        padci["indeks"].append(x+1)
                        padci["dan"].append(count_dnevi)

                    # vzponi
                    if cons_dan.iloc[x] < srednja_vrednost and cons_dan.iloc[x+1] > srednja_vrednost:
                        vzponi["indeks"].append(x+1)
                        vzponi["dan"].append(count_dnevi)

        
            # Convert lists to DataFrames
            padci_df = pd.DataFrame(padci)
            vzponi_df = pd.DataFrame(vzponi)

            # Get all unique indices from cons_dan
            vsi_indeksi = cons_dan.index

            # Extract "indeks" where "dan" matches count_dnevi
            dnevni_vzponi = vzponi_df.loc[vzponi_df["dan"] == count_dnevi, "indeks"]
            dnevni_padci = padci_df.loc[padci_df["dan"] == count_dnevi, "indeks"]

            # Convert to list for pairing
            vzponi = dnevni_vzponi.tolist()
            padci = dnevni_padci.tolist()

            # Keep track of matched indices
            matched_vzponi = set()
            matched_padci = set()

            # Find closest pairs with difference < 5 (greedy match)
            for i, v in enumerate(vzponi):
                for j, p in enumerate(padci):
                    if j in matched_padci:
                        continue  # skip if already matched
                    if abs(v - p) < 5:
                        matched_vzponi.add(i)
                        matched_padci.add(j)
                        break  # stop after first match for this vzpon

            # Remove matched values
            dnevni_vzponi = dnevni_vzponi.drop(list(matched_vzponi)).reset_index(drop=True)
            dnevni_padci = dnevni_padci.drop(list(matched_padci)).reset_index(drop=True)

            procent_padca = 0.015*SoC_max

            if dnevni_vzponi.empty:
                dnevni_vzponi = pd.Series([0])
            if dnevni_padci.empty:
                dnevni_padci = pd.Series([95])

            if dnevni_vzponi.iloc[0] > dnevni_padci.iloc[0]:
                if dnevni_padci.iloc[0] in (1, 2, 3, 4, 5):
                    dnevni_padci = dnevni_padci.iloc[1:].reset_index(drop=True)
                elif (abs(cons_dan.iloc[0] - cons_dan.iloc[dnevni_padci.iloc[0]]) <= procent_padca) and (dnevni_padci.iloc[0]<=25):
                    dnevni_padci = dnevni_padci.iloc[1:].reset_index(drop=True)
                if dnevni_padci.empty:
                    dnevni_padci = pd.Series([95])


            if dnevni_vzponi.iloc[0] < dnevni_padci.iloc[0]:
                if dnevni_vzponi.iloc[0] in (1, 2, 3, 4, 5):
                    dnevni_vzponi = dnevni_vzponi.iloc[1:].reset_index(drop=True)
                elif abs(cons_dan.iloc[0] - cons_dan.iloc[dnevni_vzponi.iloc[0]]) <= procent_padca and (dnevni_vzponi.iloc[0]<=25):
                    dnevni_vzponi = dnevni_vzponi.iloc[1:].reset_index(drop=True)
                if dnevni_vzponi.empty:
                    dnevni_vzponi = pd.Series([0])


            # Get the count of remaining elements
            vzponi_count = len(dnevni_vzponi)
            padci_count = len(dnevni_padci)
                    
            ##########################################################
            ####### določimo kaj v dnevu je prej padec ali vzpon
            triger_how_to_compute = 0
            if dnevni_vzponi[0] > dnevni_padci[0]:
                triger_how_to_compute = 2
            elif dnevni_vzponi[0] < dnevni_padci[0]:
                triger_how_to_compute = 1
            else:
                triger_how_to_compute = 2



            ###############
            #pogledamo ali imamo najprej v dnevu vzpon ali padec in na podlagi tega naredimo kaj se zgodi najprej polnjenje ali praznjenje
            if triger_how_to_compute == 1:
                ## POLNJENJE(+)    
                for i in np.arange(0, maksimalna_meja_polnjenja, 0.5): #range(int(maksimalna_meja_polnjenja)):
                    polnjenje_indexi = cons_dan.loc[ (min_vrednost + i) >= cons_dan]
                    moči_polnjenja = (min_vrednost + i)- polnjenje_indexi
                    moči_polnjenja.loc[moči_polnjenja >= bat_max] = bat_max
                    moči_polnjenja = moči_polnjenja.reindex(vsi_indeksi, fill_value=0)
                    kapaciteta_polnjenja = moči_polnjenja.sum()/4
                    kapaciteta_prva_preioda = SoC + moči_polnjenja.iloc[:dnevni_vzponi[0]].sum() / 4

                    if kapaciteta_prva_preioda > SoC_max:
                        polnjenje_indexi = cons_dan.loc[ (min_vrednost + i-0.5) > cons_dan]
                        moči_polnjenja = (min_vrednost + i-0.5)- polnjenje_indexi
                        moči_polnjenja.loc[moči_polnjenja >= bat_max] = bat_max

                        kapaciteta_polnjenja = moči_polnjenja.sum()/4
                        break

                    if kapaciteta_polnjenja > SoC_max: # state of charge po vsekem dnevu
                        polnjenje_indexi = cons_dan.loc[ (min_vrednost + i-0.5) > cons_dan]
                        moči_polnjenja = (min_vrednost + i-0.5)- polnjenje_indexi
                        moči_polnjenja.loc[moči_polnjenja >= bat_max] = bat_max

                        kapaciteta_polnjenja = moči_polnjenja.sum()/4

                        break

                indices = polnjenje_indexi.index.tolist()
                moči_polnjenja_values = moči_polnjenja.loc[moči_polnjenja.index.intersection(indices)].items()
                #moči_polnjenja_values = list(zip(indices, moči_polnjenja))
                bat_p.extend(moči_polnjenja_values)

                moči_polnjenja = moči_polnjenja.reindex(vsi_indeksi, fill_value=0)
                
                for v in range(len(dnevni_vzponi)):
                    if v == 0:
                        kapaciteta_polnjenja_prva_perioda = SoC + moči_polnjenja.iloc[:dnevni_vzponi[v]].sum() / 4
                    elif v == 1:
                        kapaciteta_polnjenja_druga_perioda = moči_polnjenja.iloc[dnevni_vzponi[v-1]:dnevni_vzponi[v]].sum() / 4

                ##PRAZNJENJE(-)
                stop_outer_loop = False
                for i in np.arange(0, minimalna_meja_praznjenja, 0.5):
                    praznjenje_indexi = cons_dan.loc[ (max_vrednost - i) <= cons_dan]
                    moči_praznjenja = (max_vrednost - i) - praznjenje_indexi
                    moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min
                    moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)
                    kapaciteta_praznjenja_prva_perioda = moči_praznjenja.iloc[:dnevni_padci[0]].sum()/4
                    kapaciteta_praznjenja = moči_praznjenja.sum() / 4

                    if SoC_min > kapaciteta_polnjenja_prva_perioda + kapaciteta_praznjenja_prva_perioda:
                        praznjenje_indexi = cons_dan.loc[ (max_vrednost - i + 0.5) < cons_dan]
                        moči_praznjenja = (max_vrednost - i + 0.5) - praznjenje_indexi
                        moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min
                        moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)

                        kapaciteta_praznjenja_prva_perioda = moči_praznjenja.iloc[:dnevni_padci[0]].sum()/4
                        kapaciteta_praznjenja = moči_praznjenja.sum() / 4
                        SoC_ostanek1 = kapaciteta_polnjenja_prva_perioda + kapaciteta_praznjenja_prva_perioda
                        stop_outer_loop = True
                    else:
                        SoC_ostanek1 = kapaciteta_polnjenja_prva_perioda + kapaciteta_praznjenja_prva_perioda


                    if padci_count >= 2:
                        kapaciteta_praznjenja_druga_perioda = moči_praznjenja.iloc[dnevni_padci[0]:dnevni_padci[1]].sum()/4
                        if SoC_min > (kapaciteta_praznjenja_druga_perioda + SoC_ostanek1 + kapaciteta_polnjenja_druga_perioda):
                            stop_outer_loop = True
                            
                            praznjenje_indexi = cons_dan.loc[ (max_vrednost - i+0.5) < cons_dan]
                            moči_praznjenja = (max_vrednost - i+0.5) - praznjenje_indexi
                            moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min 
                            moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)
                            kapaciteta_praznjenja_druga_perioda = moči_praznjenja.iloc[dnevni_padci[0]:dnevni_padci[1]].sum()/4
                            SoC_ostanek2 = SoC_ostanek1 + kapaciteta_polnjenja_druga_perioda +kapaciteta_praznjenja_druga_perioda
                            
                        else:
                            SoC_ostanek2 = SoC_ostanek1 + kapaciteta_polnjenja_druga_perioda + kapaciteta_praznjenja_druga_perioda


                    kapaciteta_praznjenja = moči_praznjenja.sum() / 4
                    if SoC_min > kapaciteta_polnjenja + SoC + kapaciteta_praznjenja:
                        praznjenje_indexi = cons_dan.loc[ (max_vrednost - i+0.5) < cons_dan]
                        moči_praznjenja = (max_vrednost - i+0.5) - praznjenje_indexi
                        moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min

                        kapaciteta_praznjenja = moči_praznjenja.sum() / 4 
                        stop_outer_loop = True


                    if stop_outer_loop:  # končaj for stavek če se izpolnjen if stavek da so periode praznjenja prekoračile periode polnjenja
                        break


                indicess = praznjenje_indexi.index.tolist()
                moči_praznjenja_values = moči_praznjenja.loc[moči_praznjenja.index.intersection(indicess)].items()
                #moči_praznjenja_values = list(zip(indicess, moči_praznjenja))
                bat_p.extend(moči_praznjenja_values)
                existing_indices = [item[0] for item in bat_p[vsi_indeksi[0]:]]


                for idx in vsi_indeksi:
                    if idx not in existing_indices:
                        # If the index is missing in bat_p, add it with a value of 0
                        bat_p.append((idx, 0)) 
                bat_p.sort(key=lambda x: x[0])

                values_last_96 = [x[1] for x in bat_p[-96:]]
                # Initialize list to store adjusted values and resulting SoC
                adjusted_bat_p = []
                StateOfCharge = SoC

                for i in range(len(values_last_96)):
                    power = values_last_96[i]
                    
                    # Predict SoC if we used this power
                    predicted_SoC = StateOfCharge + power / 4

                    # Adjust if it violates bounds
                    if predicted_SoC < SoC_min:
                        # Adjust to minimum possible charging that brings it to SoC_min
                        power = (SoC_min - StateOfCharge) * 4
                        predicted_SoC = StateOfCharge + power / 4
                    elif predicted_SoC > SoC_max:
                        # Adjust to minimum possible discharging that brings it to SoC_max
                        power = (SoC_max - StateOfCharge) * 4
                        predicted_SoC = StateOfCharge + power / 4

                    # Save adjusted value and update SoC
                    adjusted_bat_p.append(power)
                    StateOfCharge = predicted_SoC
                    bat_soc.append(StateOfCharge)


                for i in range(96):
                    bat_p[-96 + i] = (vsi_indeksi[-96 + i], adjusted_bat_p[i]) 
                SoC = StateOfCharge
                #SoC = SoC + kapaciteta_polnjenja + kapaciteta_praznjenja

            # naslednji del kode se zgodi če imamo prej padec kot pa vzopon
            elif triger_how_to_compute == 2:
                ## PRAZNJENJE(+)    
                for i in np.arange(0, minimalna_meja_praznjenja, 0.5): #range(int(maksimalna_meja_polnjenja)):
                    praznjenje_indexi = cons_dan.loc[ (max_vrednost - i) <= cons_dan]
                    moči_praznjenja = (max_vrednost - i) - praznjenje_indexi
                    moči_praznjenja.loc[moči_praznjenja <= bat_min] = bat_min
                    moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)

                    kapaciteta_praznjenja = moči_praznjenja.sum() / 4
                    kapaciteta_praznjenja_prva_perioda = SoC + moči_praznjenja.iloc[:dnevni_padci[0]].sum()/4

                    if kapaciteta_praznjenja_prva_perioda < SoC_min:
                        praznjenje_indexi = cons_dan.loc[ (max_vrednost - i + 0.5) <= cons_dan]
                        moči_praznjenja = (max_vrednost - i + 0.5) - praznjenje_indexi
                        moči_praznjenja.loc[moči_praznjenja <= bat_min] = bat_min

                        kapaciteta_praznjenja = moči_praznjenja.sum() / 4
                        break

                    if kapaciteta_praznjenja < -SoC_max: # state of charge po vsekem dnevu
                        praznjenje_indexi = cons_dan.loc[ (max_vrednost - i + 0.5) <= cons_dan]
                        moči_praznjenja = (max_vrednost - i + 0.5) - praznjenje_indexi
                        moči_praznjenja.loc[moči_praznjenja <= bat_min] = bat_min

                        kapaciteta_praznjenja = moči_praznjenja.sum() / 4
                        break


                indices = praznjenje_indexi.index.tolist()
                moči_praznjenja_values = moči_praznjenja.loc[moči_praznjenja.index.intersection(indices)].items()
                #moči_praznjenja_values = list(zip(indices, moči_praznjenja))
                bat_p.extend(moči_praznjenja_values)

                moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)

                for v in range(len(dnevni_padci)):
                    if v == 0:
                        kapaciteta_praznjenja_prva_perioda = SoC + moči_praznjenja.iloc[:dnevni_padci[v]].sum() / 4
                    elif v == 1:
                        kapaciteta_praznjenja_druga_perioda = moči_praznjenja.iloc[dnevni_padci[v-1]:dnevni_padci[v]].sum() / 4

                ##POLNJENJE(+)
                stop_outer_loop = False
                for i in np.arange(0, maksimalna_meja_polnjenja, 0.5):
                    polnjenje_indexi = cons_dan.loc[ (min_vrednost + i) >= cons_dan]
                    moči_polnjenja = (min_vrednost + i)- polnjenje_indexi
                    moči_polnjenja.loc[moči_polnjenja >= bat_max] = bat_max
                    moči_polnjenja = moči_polnjenja.reindex(vsi_indeksi, fill_value=0)
                    kapaciteta_polnjenja_prva_perioda = moči_polnjenja.iloc[:dnevni_vzponi[0]].sum()/4
                    kapaciteta_polnjenja = moči_polnjenja.sum() / 4

                    if SoC_max < kapaciteta_praznjenja_prva_perioda + kapaciteta_polnjenja_prva_perioda:
                        polnjenje_indexi = cons_dan.loc[ (min_vrednost + i - 0.5) >= cons_dan]
                        moči_polnjenja = (min_vrednost + i - 0.5)- polnjenje_indexi
                        moči_polnjenja.loc[moči_polnjenja >= bat_max] = bat_max

                        moči_polnjenja = moči_polnjenja.reindex(vsi_indeksi, fill_value=0)
                        kapaciteta_polnjenja_prva_perioda = moči_polnjenja.iloc[:dnevni_vzponi[0]].sum()/4
                        kapaciteta_polnjenja = moči_polnjenja.sum() / 4
                        SoC_ostanek1 = kapaciteta_praznjenja_prva_perioda + kapaciteta_polnjenja_prva_perioda
                        stop_outer_loop = True

                    else:
                        SoC_ostanek1 = kapaciteta_praznjenja_prva_perioda + kapaciteta_polnjenja_prva_perioda


                    if vzponi_count >= 2:
                        kapaciteta_polnjenja_druga_perioda = moči_polnjenja.iloc[dnevni_vzponi[0]:dnevni_vzponi[1]].sum()/4
                        if SoC_max < (SoC_ostanek1 + kapaciteta_praznjenja_druga_perioda + kapaciteta_polnjenja_druga_perioda):
                            stop_outer_loop = True
                            
                            polnjenje_indexi = cons_dan.loc[ (min_vrednost + i - 0.5) >= cons_dan]
                            moči_polnjenja = (min_vrednost + i - 0.5)- polnjenje_indexi
                            moči_polnjenja.loc[moči_polnjenja >= bat_max] = bat_max
                            moči_polnjenja = moči_polnjenja.reindex(vsi_indeksi, fill_value=0)
                            kapaciteta_polnjenja_druga_perioda = moči_polnjenja.iloc[dnevni_vzponi[0]:dnevni_vzponi[1]].sum()/4
                            SoC_ostanek2 = SoC_ostanek1 + kapaciteta_praznjenja_druga_perioda + kapaciteta_polnjenja_druga_perioda
                        else:
                            SoC_ostanek2 = SoC_ostanek1 + kapaciteta_praznjenja_druga_perioda + kapaciteta_polnjenja_druga_perioda    


                    kapaciteta_polnjenja = moči_polnjenja.sum() / 4
                    if SoC_max < kapaciteta_polnjenja + SoC + kapaciteta_praznjenja:
                        polnjenje_indexi = cons_dan.loc[ (min_vrednost + i - 0.5) >= cons_dan]
                        moči_polnjenja = (min_vrednost + i - 0.5)- polnjenje_indexi
                        moči_polnjenja.loc[moči_polnjenja >= bat_max] = bat_max

                        kapaciteta_polnjenja = moči_polnjenja.sum() / 4 
                        stop_outer_loop = True


                    if stop_outer_loop:  # končaj for stavek če se izpolnjen if stavek da so periode praznjenja prekoračile periode polnjenja
                        break


                indicess = polnjenje_indexi.index.tolist()
                moči_polnjenja_values = moči_polnjenja.loc[moči_polnjenja.index.intersection(indicess)].items()
                #moči_polnjenja_values = list(zip(indicess, moči_polnjenja))
                bat_p.extend(moči_polnjenja_values)

                existing_indices = [item[0] for item in bat_p[vsi_indeksi[0]:]]
                for idx in vsi_indeksi:
                    if idx not in existing_indices:
                        # If the index is missing in bat_p, add it with a value of 0
                        bat_p.append((idx, 0)) 
                bat_p.sort(key=lambda x: x[0])

                values_last_96 = [x[1] for x in bat_p[-96:]]
                # Initialize list to store adjusted values and resulting SoC
                adjusted_bat_p = []
                StateOfCharge = SoC

                for i in range(len(values_last_96)):
                    power = values_last_96[i]
                    
                    # Predict SoC if we used this power
                    predicted_SoC = StateOfCharge + power / 4

                    # Adjust if it violates bounds
                    if predicted_SoC < SoC_min:
                        # Adjust to minimum possible charging that brings it to SoC_min
                        power = (SoC_min - StateOfCharge) * 4
                        predicted_SoC = StateOfCharge + power / 4
                    elif predicted_SoC > SoC_max:
                        # Adjust to minimum possible discharging that brings it to SoC_max
                        power = (SoC_max - StateOfCharge) * 4
                        predicted_SoC = StateOfCharge + power / 4

                    # Save adjusted value and update SoC
                    adjusted_bat_p.append(power)
                    StateOfCharge = predicted_SoC
                    bat_soc.append(StateOfCharge)


                for i in range(96):
                    bat_p[-96 + i] = (vsi_indeksi[-96 + i], adjusted_bat_p[i]) 
                SoC = StateOfCharge
                

                #SoC = SoC + kapaciteta_polnjenja + kapaciteta_praznjenja
        #konec for loopa


        bat_p_dict = dict(bat_p)
        
        # Fill in missing indices with 0
        for indeksi in range(len(cons)):
            if indeksi not in bat_p_dict:
                bat_p_dict[indeksi] = 0

        bat_p = sorted(bat_p_dict.items())
        bat_p_series = pd.Series(dict(bat_p))

        # bat_df = bat_series.reset_index()
        # bat_df.columns = ['Index', 'bat_profil']  # Rename columns if needed
        # value2_series = pd.concat(cons_dnevi, ignore_index=True)

        # # Add it as a column in bat_df
        # bat_df['cons_prof'] = value2_series
        # bat_df["razlika"] = bat_df["cons_prof"]+bat_df["bat_profil"]
        # #bat_df["SoC"] = 0.0
        # bat_df["SoC"] = SoC_b + (bat_df["bat_profil"] / 4).cumsum()

        # # for i in range(len(bat_df['bat_profil'])):
        # #     if i == 0:
        # #         bat_df.loc[i, "SoC"] = SoC_b + bat_df.loc[i, 'bat_profil'] / 4  # Initial value
        # #     else:
        # #         bat_df.loc[i, "SoC"] = bat_df.loc[i-1, "SoC"] + bat_df.loc[i, 'bat_profil'] / 4
        # bat_SoC = bat_df["SoC"]
        bat_soc_series = pd.Series(bat_soc)
        return bat_p_series, bat_soc_series





            





    


      




    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    