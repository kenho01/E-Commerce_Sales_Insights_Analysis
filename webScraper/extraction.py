from scraper import Scraper
import json
import glob
import os
from datetime import datetime

scraper = Scraper()

genders = ['men', 'women']
categories = ["clothing", "shoes", "sports"]
men_brands_clothes = ["cos", "superdry", "calvin-klein", "hm", "oxgn"]
men_brands_shoes  = ['vans', 'aldo', 'birkenstock', 'converse', 'dr-martens']
brands_sports = ['adidas', 'under-armour', 'nike', 'puma', 'new-balance']
women_brands_clothes = ['cos', 'calvin-klein', 'hm', 'oxgn', 'seasalt-cornwall']
women_brands_shoes = ['aldo', 'betsy', 'birkenstock', 'converse', 'call-it-spring']
occasions = ["Casual", "Activewear", "Workwear"]

items = []

for j in men_brands_clothes:
    for k in occasions:
        t = ("men", "clothing", j , k)
        items.append(t)
        
for j in men_brands_shoes:
    for k in occasions:
        t = ("men", "shoes", j , k)
        items.append(t)

for j in women_brands_clothes:
    for k in occasions:
        t = ("women", "clothing", j , k)
        items.append(t)
for j in women_brands_shoes:
    for k in occasions:
        t = ("women", "shoes", j , k)
        items.append(t)

for i in genders:
    for j in brands_sports:
        for k in occasions:
            t = (i, "sports", j, k)
            items.append(t)

# Begin the scrape 
for i in items:
    print(i[1], i[2])
    scraper.scrape(
        gender=i[0],
        product=i[1],
        brand=i[2],
        occassion=i[3]
    )