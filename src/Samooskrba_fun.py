# -*- coding: utf-8 -*-
"""
22.1.2025

@author: tomaž DOlinar
"""

import pandas as pd
import numpy as np
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import glob
import pdb

import sys
import os
from os.path import join

class samooskrba:
    def __init__(self,consumption, production):   
        self.cons=consumption   #consumption (+) moč v kW       
        self.prod=production    #production (+) moč v kW
    
    
    def profil_samooskrbe(self,SoC_max,SoC_min,bat_max,bat_min):
        #For hourly data
        
        #SoC_max maximum battery capacity kWh
        #Soc_min minimum battery capacity kWh
        
        #bat_max battery max power kW
        #bat_min battery min power       
        
        neto_poraba=self.cons*-1
        brez_baterije=neto_poraba+self.prod #moč v kW
               

        SoC=[]
        bat_p=[]
        bat_p.append(0)
        #SoC.append(SoC_min) #morem spremenit v prvi element dataframa, da mi lahko računa naprej ireelevanten
        SoC.append(0)
        #SoC.append(1.3)
        #SoC.append(SoC_csv['SoC 3'].loc[datum_od]) #morem spremenit v prvi element dataframa, da mi lahko računa naprej ireelevanten
        x=0
        prod=0
        cons=0
        prod_brez=0
        cons_brez=0
        bat_prod=0
        bat_cons=0
        cel_interval=0
        samooskrba=0
        samooskrba_brez=0        
        


        for x in list(range(len(neto_poraba))):
            if brez_baterije[x]>=0:
                prod_brez=prod_brez+brez_baterije[x]
                samooskrba_brez=samooskrba_brez+1
            else:
                cons_brez=cons_brez-brez_baterije[x]
        for x in list(range(len(neto_poraba))):
            razlika=np.float64(self.prod[x]+neto_poraba[x]) #neto poraba ima nasproten predznak zato seštejem oba, da dobim razliko
            SoC.append(np.float64(SoC[x])+razlika*0.25)
            bat_p.append(razlika)
            cel_interval=cel_interval+1
            if -neto_poraba[x]<=self.prod[x]:
                samooskrba=samooskrba+1
                if SoC[x+1]>=SoC_max:
                    SoC[x+1]=np.float64(SoC_max)
                    bat_p[x+1]=(np.float64(SoC[x])-np.float64(SoC[x+1]))*4 #če baterija pred tem ni 100% napolnjena dodaj razliko med 100%SoC in SoC pred to iteracijo
                    bat_cons=bat_cons-bat_p[x+1]
                    prod=prod+razlika+bat_p[x+1]
                else:
                    SoC[x+1]=(np.float64(SoC[x])+razlika*0.25)
                    if razlika <= bat_max and razlika >= bat_min:
                        bat_p[x+1]=-np.float64(razlika)
                        bat_cons=bat_cons-bat_p[x+1]
                    elif razlika>bat_max:
                        bat_p[x+1]=-np.float64(bat_max)
                        prod=prod+razlika+bat_p[x+1]
                        bat_cons=bat_cons-bat_p[x+1]
                        
             
            elif -neto_poraba[x]>self.prod[x]:
                if SoC[x+1]<=SoC_min:
                    SoC[x+1]=np.float64(SoC_min)
                    bat_p[x+1]=(np.float64(SoC[x])-np.float64(SoC[x+1]))*4
                    bat_prod=bat_prod+bat_p[x+1]
                    cons=cons-razlika-bat_p[x+1]  #Ta mi da cel consumption -> poglej če je vse v redu tukaj
                else:
                    SoC[x+1]=(np.float64(SoC[x])+razlika*0.25)
                    
                    if razlika <= bat_max and razlika >= bat_min:
                        bat_p[x+1]=-np.float64(razlika)
                        if bat_p[x+1]>=0:
                            bat_prod=bat_prod+bat_p[x+1]
                            if razlika +bat_prod >=0:
                                samooskrba=samooskrba+1
                        else:
                            cons=cons-razlika-bat_p[x+1] #dodano
                        
                    elif razlika<bat_min:
                        bat_p[x+1]=-np.float64(bat_min)
                        cons=cons-(razlika+bat_p[x+1])        
                        bat_prod=bat_prod+bat_p[x+1]
          
                        
          
        bat_p=bat_p[1:]  
        bat_p_ser = pd.Series(bat_p)  
        SoC=SoC[1:] 
        
        return  bat_p_ser, SoC

    
    
    
    
    
    
    
    