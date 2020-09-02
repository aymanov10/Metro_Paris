#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 16:19:18 2019

@author: boutra
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 01:43:03 2019

@author: nous
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 12:27:36 2019

@author: nous
"""

#!/bin/env python3


import random
import Module_Fonction_final
from tkinter import *
from tkinter.messagebox import *
import time
import Module_Class_final

def rechercher():        
    Module_Fonction_final.mov(float(entr1.get()),float(entr2.get()),float(entr3.get()),float(entr4.get()))         
    #if ValueError as e :
        #showwarning('Information','Entrer un float !!!.\n Merci pour votre compréhension !')

    
if __name__ =="__main__" :

    fenetre = Tk()
    #fenetre['bg']='white'
    fenetre.title("Metro de Paris")
#    fenetre.iconbitmap(r"C:\Users\nous\Downloads\logometro.ico.")
    #fenetre.geometry("460x240")
    Label(fenetre, text = ' Latitude 1 ',relief=GROOVE).grid(row =1, column =0)
    Label(fenetre, text = ' Longitude 1 ',relief=GROOVE).grid(row =1, column =2)
    Label(fenetre, text = ' Latitude 2 ',relief=GROOVE).grid(row =1, column =4)
    Label(fenetre, text = ' Longitude 2',relief=GROOVE).grid(row =1, column =6)
    entr1 = Entry(fenetre, width = 10,font = 'bold', bg = '#FFB6B8',borderwidth=2, relief=GROOVE)
    entr2 = Entry(fenetre,width = 10,font = 'bold', bg = '#FFB6B8',borderwidth=2, relief=GROOVE)
    entr3 = Entry(fenetre,width = 10,font = 'bold', bg = '#FFB6B8',borderwidth=2, relief=GROOVE)
    entr4 = Entry(fenetre,width = 10,font = 'bold', bg = '#FFB6B8',borderwidth=2, relief=GROOVE)

    entr1.grid(row =4, column =0)
    Label(fenetre, text = '   ').grid(row =4, column =1)
    entr2.grid(row =4, column =2)
    Label(fenetre, text = '   ').grid(row =4, column =3)
    entr3.grid(row =4, column =4)
    Label(fenetre, text = '   ').grid(row =3, column =5)
    entr4.grid(row =4, column =6)
    bouton = Button(fenetre, text="Rechercher",command = rechercher)
    bouton.grid( row = 7, columnspan =7)

#
    fenetre.mainloop()
    
#    
#    start_time = time.time()   
#
#
#    a1=random.uniform(2.22,2.465)
#    a2=random.uniform(2.22,2.465)
#    b1=random.uniform(48.76,48.95)
#    b2=random.uniform(48.76,48.95)
#    
#    
#    
#    Module_Fonction_final.mov(a1,b1,a2,b2)
#    
#    print("Temps d execution : %s secondes ---" % (time.time() - start_time))
