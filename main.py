#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:00:26 2020

@author: bruno
"""


import matplotlib.pyplot as plt
from collections import OrderedDict
import requests

plt.rcParams.update({'font.size': 32})

all_data = requests.get('https://coronavirus-tracker-api.herokuapp.com/all')

assert(all_data.ok)

all_data = all_data.json()

confirmed = all_data['confirmed']
deaths = all_data['deaths']
recovered = all_data['recovered']

country = "Brazil"

country_confirmed = list(filter(lambda it: it['country'] == country, confirmed['locations']))[0]['history']
country_deaths = list(filter(lambda it: it['country'] == country, deaths['locations']))[0]['history']
country_recovered = list(filter(lambda it: it['country'] == country, recovered['locations']))[0]['history']

dates = []

for k in country_confirmed.keys():
    m,d,y = k.split('/')
    dates.append((int(d),int(m),int(y)))

dates.sort(key=lambda it: it[0] + it[1]*100)

ordered_keys = list(map(lambda it: f'{it[1]}/{it[0]}/{it[2]}', dates))
min_ordered_keys = list(map(lambda it: f'{it[0]}/{it[1]}', dates))

confirmed_ordered_values = list(map(lambda it: country_confirmed[it], ordered_keys))
deaths_ordered_values = list(map(lambda it: country_deaths[it], ordered_keys))
recovered_ordered_values = list(map(lambda it: country_recovered[it], ordered_keys))

fig, ax = plt.subplots(1,1, figsize=(25, 9), dpi=50) 

ax.plot(min_ordered_keys, confirmed_ordered_values, 'b')
ax.plot(min_ordered_keys, deaths_ordered_values, 'r--')
ax.plot(min_ordered_keys, recovered_ordered_values, 'g*')

ax.legend(["Confirmados", "Mortes", "Recuperados"])

ax.set_xticklabels(min_ordered_keys, rotation='vertical', fontsize=22)
plt.title(f"Corona - {country}")
plt.ylabel("Número de Casos")
plt.xlabel("Dias")
plt.grid()
plt.savefig(f"{country}_daily.png")
plt.close("all")
