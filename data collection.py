import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import csv
import numpy as np

factory = StemmerFactory()
stemmer = factory.create_stemmer()

kata_dasar = []
kbbi = pd.read_csv('kbbi.csv')
# kbbi.applymap(str)
# # kbbi = kbbi.apply(pd.to_numeric, errors='coerce')
# kbbi = kbbi.dropna()
for i in range(len(kbbi.index)):
    print(kbbi['kata'][i].lower())
    kata_dasar.append(stemmer.stem(kbbi['kata'][i].lower()))
print(kata_dasar)

kbbi = pd.read_csv('kbbi.csv')
stem = pd.read_csv('stem.csv')