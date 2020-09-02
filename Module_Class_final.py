# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 23:56:06 2019

@author: nous
"""
#
#from os import chdir
#chdir(r"C:\Users\nous\Desktop\Projet_2020")

import math
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from tkinter import *
import networkx as nwx
import Module_Fonction_final
import Configuration_final # import path,vit_metro, vit_marche

from Configuration_final  import zoom

#path="Paris15.csv"

#path=path
#vitesse_metro=vitesse_metro
#vitesse_marcheur= vitesse_marcheur

class Temps:
    R = 6378000               # Rayon de la terre en mètre
    PI = math.pi 
    demi_angle = 180

#    vit_marcheur= vitesse_marche
    
    def __init__(self,lat,lon):
        self.lat = lat 
        self.lon = lon
        
    def Convert(self, theta):
        return self.PI * theta / self.demi_angle
        
    def Distance(self,lat1,lon1):
        lat_a = self.Convert(self.lat)
        lon_a = self.Convert(self.lon)
        lat_b = self.Convert(lat1)
        lon_b = self.Convert(lon1)
        dist = self.R * (self.PI/2 - math.asin( math.sin(lat_b) * math.sin(lat_a) + math.cos(lon_b - lon_a) * math.cos(lat_b) * math.cos(lat_a)))
        return dist
        
    def temps(self,lat1,lon1):
        return int(self.Distance(lat1,lon1) / Configuration_final.vit_metro )
                
    def tempsmarche(self,lat1,lon1):
        return int(self.Distance(lat1,lon1) / Configuration_final.vit_marche)



   

class Ligne :
#    global path
    
    
    def __init__(self,ligne):
        self.ligne = ligne
        
    def Affiche_Ligne(self):
        couleurs=['darkred','silver','aqua','tan','gold','blue','red','yellow','m','coral','orange','lime','indigo','olive','red','coral','indigo','red','aqua']
        i=0
        fig = plt.figure(figsize=(10,10))
        for cle in self.ligne:
            Lx,Ly=self.ligne[cle][1],self.ligne[cle][2]
            plt.plot(Lx,Ly, color = couleurs[i])
            plt.scatter(Lx,Ly, color = couleurs[i],marker='o')
            i+=1
        plt.show()
        
    def Ligne_stations(self):
        ''' Dictionnaire de Lignes: stations 
        '''
        A ={}   
        for cle in self.ligne :
            A[cle]= self.ligne[cle][0]
       
        return A
        
    def temps_ligne(self):
        ''' Dictionnaire Ligne:[t(1,2), ...,t(N-1,N)]'''
        X = {}
        for cle in self.ligne:
            (Lx,Ly) = (self.ligne[cle][1],self.ligne[cle][2])
            n = len(Lx)
            Y =[]
            for j in range(n-1):
                a = Temps(Ly[j],Lx[j])
                t = a.temps(Ly[j+1],Lx[j+1])
                Y.append(t)
            X[cle]=Y
        return X
                
    def graphe(self,depart, arrivee):  
        
        ''' xo donne le tepms min entre deux points  '''
        L=self.ligne
        G = nwx.MultiGraph()
        A = self.Ligne_stations()
        
        x =Temps(depart[1],depart[2])
        y = Temps(arrivee[1],arrivee[2])
        G.add_edge(depart[0],arrivee[0], weight = x.tempsmarche(arrivee[1],arrivee[2]))
        
        n = len(A)
        t = self.temps_ligne()
        for i in A:
    
            m = len(A[i])
            for j in range(m-1):
                
                G.add_edge(A[i][j],A[i][j+1], weight = t[i][j])
                if j==0:
                    
                    td1=x.tempsmarche(L[i][1][j],L[i][2][j])   # temps entre depart et 1 station
                    ta1=y.tempsmarche(L[i][1][j],L[i][2][j])    # temps entre arrivee et 1 station
                    
                    td2=x.tempsmarche(L[i][1][j+1],L[i][2][j+1])  # temps entre depart et 2 station
                    ta2=y.tempsmarche(L[i][1][j+1],L[i][2][j+1])   # temps entre depart et 1 station
                    
                    G.add_edge(depart[0],A[i][0], weight = td1)
                    G.add_edge(arrivee[0],A[i][0], weight = ta1)
                    G.add_edge(depart[0],A[i][1], weight = td2)
                    G.add_edge(arrivee[0],A[i][1], weight = ta2)
                else:
                    
                    td=x.tempsmarche(L[i][1][j+1],L[i][2][j+1])
                    ta=y.tempsmarche(L[i][1][j+1],L[i][2][j+1])
                    G.add_edge(depart[0],A[i][j+1], weight = td)
                    G.add_edge(arrivee[0],A[i][j+1], weight = ta)
    
        xo = nwx.floyd_warshall(G)
        return xo
    
    def plus_court_chemin(self,depart,arrivee) :
#        L=self.ligne
        xo= self.graphe(depart, arrivee)
        station1 = depart[0] 
        station2 = arrivee[0] 
        v = xo[station1][station2] 
        
        dic={}
       
        p = xo[station1][station2]    
        for station in Module_Fonction_final.lignes_metro(Configuration_final.path)[1]: 
#            print(station)
            v1 = xo[station1][station]
            
            v2 = xo[station][station2]
            if v1 + v2 ==  p:
            
               dic[xo[station1][station]]=station
    
        liste=np.sort(list(dic.keys()))
        l = [station1]
        for i in liste:
            
            l.append(dic[i])
        l.append(station2)
        
        if len(l)>2:
            stat1=l[2]
            i=0
            while stat1 != station2:
                Voi = Station(stat1)
                list1=Voi.voisin()[1]
                list2=l[3+i:len(l)]
                sss=list(set(list1).intersection(list2))
                p = xo[stat1][station2]    
                for station in sss:       
                    v1 = xo[stat1][station]
                    v2 = xo[station][station2]
                    if v1 + v2 !=  p:
                        
                        
                         
                       l.pop(station)
                i+=1
                stat1 = l[2+i]
        if len(l)==3:
            l=['Point_depart',  'Point_arrivee']
          
        return l,v
            
class Station :
    
    
    def __init__(self,station):
        self.station = station
        
    def voisin(self):
        Lignes= Module_Fonction_final.lignes_metro(Configuration_final.path)[0]
        l=[[],[],[],[]]
        # [[liste de L contenant Station],[Station voisines],[ Lat, lon]]
        for cle in Lignes:
            if self.station in Lignes[cle][0]:
                d = Lignes[cle][0].index(self.station)
                l[0]+=[cle]
                l[2].append(Lignes[cle][1][d])
                l[3].append(Lignes[cle][2][d])
                if d == 0 :
                    l[1].append(Lignes[cle][0][d+1])
                elif d == len(Lignes[cle][0])-1:
                    l[1].append(Lignes[cle][0][d-1])
                else :
                    l[1].append(Lignes[cle][0][d+1])
                    l[1].append(Lignes[cle][0][d-1])
        return l
    


        
class Trajet: 
    

    def __init__(self,Chemin):
        self.Chemin = Chemin
                
    def corresp(self):
        Lignes= Module_Fonction_final.lignes_metro(Configuration_final.path)[0]
        n=len(self.Chemin)
        a=[]# liste de listes des lignes entre deux stations sucssives du chemin
        stock=[]
#        print(self.Chemin)
        if n<=3:
              Lignes_corresp=['De votre point de depart allez directement vers votre destination sans prendre le metro']
        else:
            
            for i in np.arange(1,n-2,1):
                
                S0 = Station(self.Chemin[i])
                S1 = Station(self.Chemin[i+1])
                list1 = S0.voisin()[0]
                list2 = S1.voisin()[0]
    
                s=list(set(list1).intersection(list2))
        #            print(s)
                b=s
                if len(s)==1:
                    a.append(s)
                
                if len(s)>1:
                    
                     b =[]
                     
                     for k in range(len(s)):
                                          
                        s1=Lignes[s[k]][0].index(self.Chemin[i])
                        s2=Lignes[s[k]][0].index(self.Chemin[i+1])
                        
#                        if abs(s1-s2)==1:
        
                        b=[s[k]]
                            
        #                        print(b)
                     a.append(b) # liste de listes des lignes entre deux stations sucssives du chemin
            a=Module_Fonction_final.arbre(a)
  
            Lignes_corresp={}
            
            
            Lignes_corresp[a[0][0]]= Lignes[a[0][0]]
               
            for i in range(len(a)-1):
                if a[i]!=a[i+1]:
                    
                    stock.append(i)
                    Lignes_corresp[a[i+1][0]]= Lignes[a[i+1][0]]
                
    
        return   Lignes_corresp,a,stock 
    
   
    
    def guide(self,depart,arrivee,Durreé):
        Lignes = Module_Fonction_final.lignes_metro(Configuration_final.path)[0]
#        Duree=Ligne.plus_court_chemin(Lignes,depart,arrivee)[1]
        
        Lignes_corresp,a,stock=Trajet.corresp(self)
        if Lignes_corresp==['De votre point de depart allez directement vers votre destination sans prendre le metro']:
            parahgraphe=(f" {Lignes_corresp[0]}")
            parahgraphe = f"{parahgraphe}\n"
            parahgraphe+=(f" Il vous faut {int(Durreé/60) } minutes et {Durreé-60*int(Durreé/60)  } secondes .")
            
            return parahgraphe
        else:
            
            stock=[]
            for i in range(len(a)-1):
                    if a[i]!=a[i+1]:
                        
                        stock.append(i)
                       
                            
            parahgraphe=(f"   Allez à la station {self.Chemin[1]} pour prendre la ligne {a[0][0]}")
            parahgraphe = f"{parahgraphe}\n"
            for i in range(len(stock)):
                parahgraphe+=(f" jusqu'à la station {self.Chemin[stock[i]+2]}, prenez la ligne {a[stock[i]+1][0]}")
                parahgraphe = f"{parahgraphe}\n"
            parahgraphe+=(f" vous descendrez à la station {self.Chemin[len(a)+1]  } et allez vers  votre destination !")    
            parahgraphe = f"{parahgraphe}\n"
            parahgraphe+=(f" Il vous faut {int(Durreé/60) } minutes et {Durreé-60*int(Durreé/60)  } secondes .")
            
            return parahgraphe

        
    def representation_graphique(self,Lignes_corresp,depart,arrivee,Durreé):
        Lignes= Module_Fonction_final.lignes_metro(Configuration_final.path)[0]
        Lignes_corresp,a,stock=Trajet.corresp(self)
        if Lignes_corresp!=['De votre point de depart allez directement vers votre destination sans prendre le metro']:
       
            abscisses=[depart[1]]
            ordonnees=[depart[2]]
            for station in self.Chemin[1:len(self.Chemin)-1] :
#                if station!=depart[0] or  station!=arrivee[0]:
                S0 = Station(station)
                 
                r=S0.voisin()
                lat=r[2][0]
                lon=r[3][0]
                abscisses.append(lat)
                ordonnees.append(lon)
                    
            abscisses.append(arrivee[1])
            ordonnees.append(arrivee[2])        
           
                    
            v_x=[]
            v_y=[]
            for n in range(len(abscisses)-1):
                v_x.append((abscisses[n+1]-abscisses[n])/0.15)
                v_y.append((ordonnees[n+1]-ordonnees[n])/0.15)
            plt.figure(figsize=(10,10))
            
            plt.subplots_adjust(left=0.06, bottom=0.16, right=0.99, top=0.92,
                        wspace=0.2, hspace=None)
            #------------------------------
           
            plt.scatter(abscisses,ordonnees,marker='o')
            
            plt.xlabel('Latitude', fontsize=14)
            plt.ylabel('longitude', fontsize=14)
            plt.xlim(2.2,2.465)
            for i in range(0,len(v_x),1):
                Vec=plt.quiver(abscisses[i], ordonnees[i] ,v_x[i] , v_y[i],
                scale_units='xy',angles='xy', scale=10)
                plt.quiverkey(Vec,1,1,20,label='v',labelcolor='red')
            
            plt.text(abscisses[0],ordonnees[0],self.Chemin[0], fontsize=8, color='r')    
            plt.text(abscisses[1],ordonnees[1],self.Chemin[1], fontsize=8)
            
            for i in range(len(stock)):
                plt.text(abscisses[stock[i]+2],ordonnees[stock[i]+2],self.Chemin[stock[i]+2], fontsize=8)
                
            plt.text(abscisses[len(a)+1],ordonnees[len(a)+1],self.Chemin[len(a)+1], fontsize=8)
            plt.text(abscisses[len(self.Chemin)-1],ordonnees[len(self.Chemin)-1],self.Chemin[len(self.Chemin)-1], fontsize=8, color='r')
            #------------------------------
            couleurs=['darkred','silver','aqua','tan','gold','blue','red','yellow','m','coral','orange','lime','indigo','olive','red','coral','indigo','red','aqua']
            i=0
            for cle in Lignes_corresp:
                
                    Lx=Lignes_corresp[cle][1]
                    Ly=Lignes_corresp[cle][2]
        #            print(Lx)
                    plt.plot(Lx,Ly, color = couleurs[i], label=cle)
                    plt.scatter(Lx,Ly, color = couleurs[i],marker='o')
                    plt.legend()
                    i+=1
    
        else  :
            
            
        
        
            abscisses=[depart[1]]
            ordonnees=[depart[2]]
            abscisses.append(arrivee[1])
            ordonnees.append(arrivee[2])        
           
                    
            v_x=[]
            v_y=[]
            for n in range(len(abscisses)-1):
                v_x.append((abscisses[n+1]-abscisses[n])/0.15)
                v_y.append((ordonnees[n+1]-ordonnees[n])/0.15)
            plt.figure(figsize=(10,10))
            
            plt.subplots_adjust(left=0.06, bottom=0.16, right=0.99, top=0.92,
                        wspace=0.2, hspace=None)
            #------------------------------
           
            plt.scatter(abscisses,ordonnees,marker='o')
           
            plt.xlabel('Latitude ')
            plt.ylabel('Altitude z en (m)')
            plt.xlim(0.95*min(abscisses),1.05*max(abscisses))
            for i in range(0,len(v_x),1):
                Vec=plt.quiver(abscisses[i], ordonnees[i] ,v_x[i] , v_y[i],
                scale_units='xy',angles='xy', scale=10)
                plt.quiverkey(Vec,1,1,20,label='v',labelcolor='red')
                plt.text(abscisses[i],ordonnees[i],self.Chemin[i], fontsize=6)
            #------------------------------
            
                    
        plt.title(Trajet.guide(self,depart,arrivee,Durreé)  , fontsize=12)   
        plt.show()

        
        

        
class Animation:  
     
    global Arret,lat,lon,RAYON,HAUTEUR,LARGEUR,n,zoom
    Arret = True
    LARGEUR = 600
    HAUTEUR = 450
    RAYON = 5
    n=0
  
    
    def __init__(self,Chemin,depart,arrivee,Canevas, Mafenetre):
        self.Chemin = Chemin
        self.depart = depart
        self.arrivee = arrivee
        self.Canevas = Canevas
        self.Mafenetre = Mafenetre
        
    def deplacement(self):
        """ Déplacement de la balle """
        global Arret,lat,lon,RAYON,HAUTEUR,LARGEUR,n,zoom
        
#        Chemin=Ligne.plus_court_chemin(self.depart,self.arrivee)[0]
        
        if n<len(self.Chemin)-1:
            if n==0:
                lat=zoom*(self.depart[1]-2.2)
                lon=zoom*(self.depart[2]-48.74)
            
            else:
                
                S0 = Station(self.Chemin[n])
                 
                r=S0.voisin()
    
                lat=zoom*(r[2][0]-2.2)
                lon=zoom*(r[3][0]-48.74)
                self.Canevas.create_oval(lat-RAYON,lon-RAYON,lat+RAYON,lon+RAYON, outline='red', fill='black')
        if n==len(self.Chemin)-1:
            lat=zoom*(self.arrivee[1]-2.2)
            lon=zoom*(self.arrivee[2]-48.74)
            self.Canevas.create_oval(lat-RAYON,lon-RAYON,lat+RAYON,lon+RAYON, outline='red', fill='red')
    
        n+=1
        if n==len(self.Chemin):
            n=0
    #    Canevas.coords(Balle,lat-RAYON,lon-RAYON,lat+RAYON,lon+RAYON)
        self.Canevas.create_oval(lat-RAYON,lon-RAYON,lat+RAYON,lon+RAYON, outline='red', fill='black')
        # mise à jour toutes les 50 ms
#       
        if Arret == False:
            # appel de la fonction Cercle() après une pause de 50 millisecondes
            self.Mafenetre.after(200,self.deplacement)
    
    def Arreter(self):
    	""" Arrêt de l'animation """
    	global Arret,lat,lon,RAYON,HAUTEUR,LARGEUR,n
    	Arret = True
    
    def Demarrer(self):
        """ Démarre l'animation """
        global Arret,lat,lon,RAYON,HAUTEUR,LARGEUR,Chemin,n
    #    Canevas.delete(ALL)
        
            
        if Arret == True:
            Arret = False
            self.deplacement() # un seul appel à cette fonction