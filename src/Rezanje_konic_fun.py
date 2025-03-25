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
                # Ensure x-3 and x+3 are within bounds
                if (x  >= 0) and (x+1 < len(cons_dan)):
                    # padci
                    if cons_dan.iloc[x] >= srednja_vrednost and cons_dan.iloc[x+1] <= srednja_vrednost:
                        padci["indeks"].append(x+1)
                        padci["dan"].append(count_dnevi)

                    # vzponi
                    if cons_dan.iloc[x] <= srednja_vrednost and cons_dan.iloc[x+1] >= srednja_vrednost:
                        vzponi["indeks"].append(x+1)
                        vzponi["dan"].append(count_dnevi)

            padci_df = pd.DataFrame(padci)
            #print(padci_df)
            
            vzponi_df = pd.DataFrame(vzponi)
            #print(vzponi_df)


            # Najprej pridobi vse unikatne indekse iz cons_dan
            vsi_indeksi = cons_dan.index
            dnevni_vzponi = vzponi_df.loc[vzponi_df["dan"] == count_dnevi,"indeks"]
            # Preoblikuj moči_polnjenja, da vključuje vse indekse, z manjkajočimi vrednostmi nastavljenimi na 0


            ##########################################################


            ## POLNJENJE(+)    
            for i in np.arange(0, maksimalna_meja_polnjenja, 0.5): #range(int(maksimalna_meja_polnjenja)):
                polnjenje_indexi = cons_dan.loc[ (min_vrednost + i) >= cons_dan]
                moči_polnjenja = (min_vrednost + i)- polnjenje_indexi
                moči_polnjenja.loc[moči_polnjenja >= bat_max] = bat_max
                #moči_polnjenja = moči_polnjenja.reindex(vsi_indeksi, fill_value=0)

                kapaciteta = moči_polnjenja.sum()/4
                kapaciteta_prva_preioda = SoC + moči_polnjenja.iloc[:dnevni_vzponi[0]].sum() / 4

                if kapaciteta_prva_preioda > SoC_max:
                    polnjenje_indexi = cons_dan.loc[ (min_vrednost + i-0.5) > cons_dan]
                    moči_polnjenja = (min_vrednost + i-0.5)- polnjenje_indexi
                    moči_polnjenja.loc[moči_polnjenja >= bat_max] = bat_max
                    #moči_polnjenja = moči_polnjenja.reindex(vsi_indeksi, fill_value=0)

                    kapaciteta = moči_polnjenja.sum()/4
                    break



                if kapaciteta > SoC_max: # state of charge po vsekem dnevu
                    polnjenje_indexi = cons_dan.loc[ (min_vrednost + i-0.5) > cons_dan]
                    moči_polnjenja = (min_vrednost + i-0.5)- polnjenje_indexi
                    moči_polnjenja.loc[moči_polnjenja >= bat_max] = bat_max
                    #moči_polnjenja = moči_polnjenja.reindex(vsi_indeksi, fill_value=0)

                    kapaciteta = moči_polnjenja.sum()/4


                    #indices = polnjenje_indexi.index.tolist()
                    #moči_polnjenja_values = list(zip(indices, moči_polnjenja))
                    #bat_p.extend(moči_polnjenja_values)

                    break
            indices = polnjenje_indexi.index.tolist()
            moči_polnjenja_values = list(zip(indices, moči_polnjenja))
            bat_p.extend(moči_polnjenja_values)

            moči_polnjenja = moči_polnjenja.reindex(vsi_indeksi, fill_value=0)
            
            for v in range(len(dnevni_vzponi)):
                if v == 0:
                    kapaciteta_prva_preioda = SoC + moči_polnjenja.iloc[:dnevni_vzponi[v]].sum() / 4
                elif v == 1:
                    kapaciteta_druga_preioda = moči_polnjenja.iloc[dnevni_vzponi[v-1]:dnevni_vzponi[v]].sum() / 4
                elif v == 2:
                    kapaciteta_tretja_preioda =moči_polnjenja.iloc[dnevni_vzponi[v-1]:dnevni_vzponi[v]].sum() / 4
            
            dnevni_padci = padci_df.loc[padci_df["dan"] == count_dnevi,"indeks"]
            if len(dnevni_padci)==0:
                dnevni_padci = [cons_dan.index[-1]]
            for p in range(len(dnevni_padci)):
                padci_count = p
            ##PRAZNJENJE(-)
            stop_outer_loop = False
            for i in np.arange(0, minimalna_meja_praznjenja, 0.5):
                praznjenje_indexi = cons_dan.loc[ (max_vrednost - i) <= cons_dan]
                moči_praznjenja = (max_vrednost - i) - praznjenje_indexi
                #moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)
                moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min
                kapaciteta_praznjenja_prva_perioda = moči_praznjenja.iloc[:dnevni_padci[0]].sum()/4
                kapaciteta_praznjenja = moči_praznjenja.sum() / 4

                if SoC_min > kapaciteta_prva_preioda + kapaciteta_praznjenja_prva_perioda:
                    praznjenje_indexi = cons_dan.loc[ (max_vrednost - i + 0.5) < cons_dan]
                    moči_praznjenja = (max_vrednost - i + 0.5) - praznjenje_indexi
                    #moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)
                    moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min


                    kapaciteta_praznjenja_prva_perioda = moči_praznjenja.iloc[:dnevni_padci[0]].sum()/4
                    kapaciteta_praznjenja = moči_praznjenja.sum() / 4
                    SoC_ostanek1 = kapaciteta_prva_preioda +kapaciteta_praznjenja_prva_perioda


                    stop_outer_loop = True

                else:
                    SoC_ostanek1 = kapaciteta_prva_preioda + kapaciteta_praznjenja_prva_perioda


                if padci_count >= 1:
                    kapaciteta_praznjenja_druga_perioda = moči_praznjenja.iloc[dnevni_padci[0]:dnevni_padci[1]].sum()/4
                    if SoC_min > (kapaciteta_druga_preioda + SoC_ostanek1 + kapaciteta_praznjenja_druga_perioda):
                        stop_outer_loop = True
                        for i in np.arange(0, minimalna_meja_praznjenja, 0.5):
                            praznjenje_indexi = cons_dan.loc[ (max_vrednost - i) < cons_dan]
                            moči_praznjenja = (max_vrednost - i) - praznjenje_indexi
                            #moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)
                            moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min

                            kapaciteta_praznjenja_druga_perioda = moči_praznjenja.iloc[dnevni_padci[0]:dnevni_padci[1]].sum()/4
                            if SoC_min > (kapaciteta_druga_preioda + SoC_ostanek1 + kapaciteta_praznjenja_druga_perioda):
                                praznjenje_indexi = cons_dan.loc[ (max_vrednost - i+0.5) < cons_dan]
                                moči_praznjenja = (max_vrednost - i+0.5) - praznjenje_indexi
                                #moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)
                                moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min 

                                kapaciteta_praznjenja_druga_perioda = moči_praznjenja.iloc[dnevni_padci[0]:dnevni_padci[1]].sum()/4
                                SoC_ostanek2 = SoC_ostanek1 + kapaciteta_druga_preioda +kapaciteta_praznjenja_druga_perioda
                                break
                            else:
                                SoC_ostanek2 = SoC_ostanek1 + kapaciteta_druga_preioda + kapaciteta_praznjenja_druga_perioda
                    SoC_ostanek2 = SoC_ostanek1 + kapaciteta_druga_preioda + kapaciteta_praznjenja_druga_perioda    
                

                # if padci_count == 2:
                #     kapaciteta_praznjenja_tretja_perioda = moči_praznjenja.iloc[dnevni_padci[1]:dnevni_padci[2]].sum()/4
                #     if SoC_min > (kapaciteta_tretja_preioda + SoC_ostanek2 + kapaciteta_praznjenja_tretja_perioda):
                #         for i in np.arange(0, minimalna_meja_praznjenja, 0.5):
                #             praznjenje_indexi = cons_dan.loc[ (max_vrednost - i) < cons_dan]
                #             moči_praznjenja = (max_vrednost - i) - praznjenje_indexi
                #             moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)
                #             moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min

                #             kapaciteta_praznjenja_tretja_perioda = moči_praznjenja.iloc[dnevni_padci[1]:dnevni_padci[2]].sum()/4
                #             if SoC_min > (kapaciteta_tretja_preioda + SoC_ostanek2 + kapaciteta_praznjenja_tretja_perioda):
                #                 praznjenje_indexi = cons_dan.loc[ (max_vrednost - i+0.5) < cons_dan]
                #                 moči_praznjenja = (max_vrednost - i+0.5) - praznjenje_indexi
                #                 moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)
                #                 moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min

                #                 kapaciteta_praznjenja_tretja_perioda = moči_praznjenja.iloc[dnevni_padci[1]:dnevni_padci[2]].sum()/4
                #                 SoC_ostanek3 = SoC_ostanek2 + kapaciteta_tretja_preioda +kapaciteta_praznjenja_tretja_perioda
                #             else:
                #                 SoC_ostanek3 = SoC_ostanek2 + kapaciteta_tretja_preioda + kapaciteta_praznjenja_tretja_perioda

                kapaciteta_praznjenja = moči_praznjenja.sum() / 4
                if SoC_min > kapaciteta + SoC + kapaciteta_praznjenja:
                    praznjenje_indexi = cons_dan.loc[ (max_vrednost - i+0.5) < cons_dan]
                    moči_praznjenja = (max_vrednost - i+0.5) - praznjenje_indexi
                    #moči_praznjenja = moči_praznjenja.reindex(vsi_indeksi, fill_value=0)
                    moči_praznjenja.loc[moči_praznjenja < bat_min] = bat_min

                    kapaciteta_praznjenja = moči_praznjenja.sum() / 4 
                    stop_outer_loop = True


                if stop_outer_loop:  # končaj for stavek če se izpolnjen if stavek da so periode praznjenja prekoračile periode polnjenja
                    break


            # Drop indices where values are 0
            # Filter out indices where values are 0
            #moči_praznjenja = moči_praznjenja.loc[moči_praznjenja != 0]
            #print(moči_praznjenja)
            # for i in range(len(moči_praznjenja)):
            #     print(moči_praznjenja.iloc[i])

            indicess = praznjenje_indexi.index.tolist()
            moči_praznjenja_values = list(zip(indicess, moči_praznjenja))
            bat_p.extend(moči_praznjenja_values)

            SoC = SoC + kapaciteta + kapaciteta_praznjenja

        #konec for loopa


        bat_p_dict = dict(bat_p)

        # Fill in missing indices with 0
        for indeksi in range(len(cons)):
            if indeksi not in bat_p_dict:
                bat_p_dict[indeksi] = 0

        bat_p = sorted(bat_p_dict.items())
        bat_series = pd.Series(dict(bat_p))

        bat_df = bat_series.reset_index()
        bat_df.columns = ['Index', 'bat_profil']  # Rename columns if needed
        value2_series = pd.concat(cons_dnevi, ignore_index=True)

        # Add it as a column in bat_df
        bat_df['cons_prof'] = value2_series
        bat_df["razlika"] = bat_df["cons_prof"]+bat_df["bat_profil"]
        #bat_df["SoC"] = 0.0
        bat_df["SoC"] = SoC_b + (bat_df["bat_profil"] / 4).cumsum()

        # for i in range(len(bat_df['bat_profil'])):
        #     if i == 0:
        #         bat_df.loc[i, "SoC"] = SoC_b + bat_df.loc[i, 'bat_profil'] / 4  # Initial value
        #     else:
        #         bat_df.loc[i, "SoC"] = bat_df.loc[i-1, "SoC"] + bat_df.loc[i, 'bat_profil'] / 4
        bat_SoC = bat_df["SoC"]
        return bat_series, bat_SoC





            





    


      




    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    