# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 18:51:05 2022

@author: tamme
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


float_formatter = "{:.10f}".format
float_formatter2 = "{:.2f}".format

fig = plt.figure()
ax = fig.add_subplot(1,1,1)


st.title('Kalojen pituuden ja painon välisen riippuvuuden määrittävä ohjelma')

st.text('TOIMINTAOHJEET')
st.text('1. Luo csv-päätteinen tekstitiedosto. Jos et tiedä, mikä csv-tiedosto \n on, voit katsoa tästä mallia: https://fi.wikipedia.org/wiki/CSV')
st.text('2. Kirjaa tiedostoon pituudet (mm) ja niitä vastaavat painot (g) pilkulla\n toisistaan erotettuna siten, että pituudet ovat vasemmalla puolella \n ja painot oikealla puolella. Tarvitset muutamia kymmeniä havaintopareja, jotta \n parametrit kyetään määrittämään tarkasti.')
st.text('3. Käytä desimaalipilkun sijaan pistettä')
st.text('4. Älä käytä sarakeotsikoita')



data=st.file_uploader('Lataa csv-tiedosto',type=["csv"], accept_multiple_files=False)

if data==None:
    data = "tyhjä.csv"

df = pd.read_csv(data, names=["pituus", "paino"])

if df.empty:
    st.write("Ei valittua pituus-paino tietoa")

st.title("Data")

df

plt.xlabel("Pituus (mm)")
plt.ylabel("Paino (g)")

def func(l,a,b):
    return a*pow(l,b)

if len(df)>1:
    popt, pcov = curve_fit(func, df["pituus"], df["paino"],p0=(0.005,2.5))

    st.title("Tulokset")
    st.text("Parametri a: "+str(float_formatter(popt[0])))
    st.text("Parametri b: "+str(float_formatter(popt[1])))
    st.text("Paino (g) = " + str(float_formatter(popt[0]))+ "*pituus (mm)^" + str(float_formatter(popt[1])))
    plt.plot(df["pituus"], df["paino"], 'bo')
    
   
    xFit = np.arange(0.0, max(df['pituus']), 0.01)
    plt.plot(xFit, func(xFit, *popt), 'r')
    plt.show()
   
    
    residuals = df["paino"]- func(df["pituus"], *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((df["paino"]-np.mean(df["paino"]))**2)
    r_squared = 1 - (ss_res / ss_tot)
    st.text("Mallin selitysaste: " + str(float_formatter2(r_squared)))
    
    st.write(fig)

