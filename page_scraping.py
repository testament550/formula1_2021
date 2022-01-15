# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 16:27:26 2022

@author: Panagiotis
"""

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd



#web scraping the page links
req = Request("https://www.formula1.com/en/results.html/2021/races.html")
html_page = urlopen(req)


soup = BeautifulSoup(html_page, "lxml")

links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

# print(links)

filter = "/en/results.html/2021/races/1" 
cleaned_list = []
for i in links:
    if i != None:
        if filter in i and i not in cleaned_list:
            cleaned_list.append(i)

links_2021 = ["https://www.formula1.com/"+i for i in cleaned_list]

#building data
data = []
for i in links_2021:
    data.append(pd.read_html(i))

races = []
race_counter = 1
for race in data:
    cleaned_race = race[0][['Driver','PTS']]
    for i in range(len(cleaned_race)):
        cleaned_race['Driver'][i] = cleaned_race['Driver'][i][-3::]
    cleaned_race.set_index('Driver',inplace=True) #set indexes the name of driver
    cleaned_race.rename({'PTS' : str(race_counter)}, axis = 1, inplace = True)
    race_counter += 1
    races.append(cleaned_race)

drivers = set(races[1].index)
for i in races:
    for name in list(i.index):
        if name not in drivers:
            drivers.add(name)

points = pd.DataFrame(drivers)
points.set_index(points[0],inplace=True)
points = points.join(races[0])
points = points.drop(labels=[0],axis=1)
for i in range(1,len(races)):
    points = points.join(races[i])
