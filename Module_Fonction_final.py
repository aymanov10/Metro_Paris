# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 05:20:58 2019

@author: nous
"""
import math


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from tkinter import *
import networkx as nwx
import Module_Class_final
import Configuration_final

#from os import chdir
#chdir(r"C:\Users\nous\Desktop\Projet_2020")



def Traitement_de_données(df):
    df = df.loc[:,['ligne','nom_gare', 'Geo Point']]
    df.reset_index(drop = True, inplace = True)
    df["x"] = np.nan
    df["y"] = np.nan   
    for index, row in df.iterrows():
        arr = str(row["Geo Point"]).split(',')
        df.loc[[index], ["x"]] = arr[0]
        df.loc[[index], ["y"]] = arr[1]   
    df = df.sort_values(by = 'y', ascending = True) 
    del (df['Geo Point'])
    return df
    
def concatenation():
    l =[]
    n = range(1,16)
    for i in n :
        path = f"/users/mmath/kamalsem/Téléchargements/ligne{i}.csv"
        df = pd.read_csv(path, sep = ';')
        d = Traitement_de_données(df)
        l.append(d)
    df = pd.concat(l, ignore_index=True)
    df1= df.to_csv(Configuration_final.path, header = False , index = False)
    return df
    

def lignes_metro(path): 
#    global path
    with open(path,"r") as f:
    #f.readline()
        LL=f.readlines()

#        #le dictionnaire sera constitué de :
#         #   cle : numero de la ligne
#          #  valeurs: liste constituee de :
#           # Liste des noms des stations
#            #Liste des abscisses x
#            #Liste des abscisses y
# 

        ligne=[ligne.strip("\n").split(",") for ligne in LL]  
        Lnom1=np.unique([ligne[0] for ligne in ligne])  
        Lignes={i:[[],[],[]] for i in Lnom1 }
        Liste_stations=[]
        for ligne in LL:
            ligne=ligne.strip("\n").split(",")
#            print(ligne)
            Lnom,Lx,Ly=Lignes[ligne[0]] 
            Lnom.append(ligne[1])
            Lx.append(float(ligne[3]))
            Ly.append(float(ligne[2]))
            Lignes[ligne[0]]=[Lnom,Lx,Ly]
            Liste_stations=Liste_stations+Lnom
            Liste_stations=list(np.unique(Liste_stations))
        
#        Noeud=Noeud #+['Point_arrivee']
        return Lignes,Liste_stations
#
def arbre(a):
    
    
    k=1
    for i in range(len(a)):

        k=k*len(a[i])
   
    if k!=1:
       
        A=[ a for j in range(k)]  
        A=np.array(A)
        
        for j in range(len(a)):
            
            for i in range(k):
                x=a[j]*int(k/len(a[j]))
                if len(a[j])==1:
                    A[i,j]=list([x[i]])
                else:
                    
                    A[i,j]=list(x[i])
#                print(A)    
        N={}
        for n in range(len(A)):
        #    n=2
            v=A[n]
            num=sum((v[0:len(a)-1]!=v[1:len(a)])*1)
           
            N[num]=n
        ii=np.sort(list(N.keys()))   
        index=N[ii[0]]
        a=list(A[index]) 

    return a



def mov(a1,b1,a2,b2):
    
#    global path
    depart=['Point_depart',a1,b1]
    arrivee=['Point_arrivee',a2,b2]
    
#    path = "Paris15.csv"
    Lignes,Noeud= lignes_metro(Configuration_final.path)
    L=Module_Class_final.Ligne(Lignes)
    L=Module_Class_final.Ligne(Lignes)
    Chemin,Durreé=L.plus_court_chemin( depart, arrivee)
    T=Module_Class_final.Trajet(Chemin)
    Lignes_corresp,a,stock=T.corresp()
    T.representation_graphique(Lignes_corresp,depart,arrivee,Durreé)
#    T.guide(depart,arrivee,Durreé)
    zoom=1800
    
    LARGEUR = 600
    HAUTEUR = 450
    RAYON = 5 
    lat=zoom*(depart[1]-2.2)
    lon=zoom*(depart[2]-48.74)
       
    
    Arret = True
    # Création de la fenêtre principale
    Mafenetre = Tk()
    Mafenetre.title("Je me déplace ")
    
    # Création d'un widget Canvas
    Canevas = Canvas(Mafenetre,height=HAUTEUR,width=LARGEUR,bg='white')
    Canevas.pack(padx=20,pady=20)
    W=Module_Class_final.Animation(Chemin,depart, arrivee,Canevas, Mafenetre)
    # Création d'un objet graphique
    k=0
    kk=0
    
    Balle = Canevas.create_oval(lat-RAYON,lon-RAYON,lat+RAYON,lon+RAYON,width=1,fill='black')
    
    lat=zoom*(arrivee[1]-2.2)
    lon=zoom*(arrivee[2]-48.74)
    Balle = Canevas.create_rectangle(lat-RAYON,lon-RAYON,lat+RAYON,lon+RAYON,width=1.5,fill='black')
    if Lignes_corresp!=['De votre point de depart allez directement vers votre destination sans prendre le metro']:
     
        for cle in Lignes_corresp:
            couleurs=['darksalmon','silver','aqua','tan','gold','blue','red','yellow','m','coral','orange','lime','indigo','olive','red','coral','indigo','red','aqua']
            ii=0
            for lat1 in Lignes[cle][1]:
                
                lat=zoom*(lat1-2.2)
        #        s1=Lignes_corresp[cle][1].index(lat1)
                lon=zoom*(Lignes[cle][2][ii]-48.74)
                ii+=1
                
                Balle = Canevas.create_oval(lat-RAYON,lon-RAYON,lat+RAYON,lon+RAYON,width=1,fill=couleurs[kk])
                k+=1
            kk+=1
    BoutonGo = Button(Mafenetre, text ='Démarrer', command = W.Demarrer)
    BoutonGo.pack(side = LEFT, padx = 10, pady = 10)
    
    # Création d'un widget Button (bouton Arrêter)
    BoutonArreter = Button(Mafenetre, text ='Arrêter', command = W.Arreter)
    BoutonArreter.pack(side = LEFT, padx = 5, pady = 5)
    
    # Création d'un widget Button (bouton Quitter)
    BoutonQuitter = Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy)
    BoutonQuitter.pack(side = LEFT, padx = 5, pady = 5)
      
    
    Mafenetre.mainloop()