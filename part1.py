
# coding: utf-8

import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
import re
import string
import inflect
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# import data
data = pd.read_excel('Data_Science_Internship_Assignment.xlsx', sheet_name='Data')

# data prepossessing

## lower data
tags = data["TAGLINE"].str.lower()
tags = list(tags)

## remove number
def remove_numbers(tags):
    result = re.sub(r'\d+', '', tags)
    return result

## remove URL
def remove_URL(tags):
    return re.sub(r"http\S+", "", tags)


## remove above
def remove_tags(tags):
    tags = remove_numbers(tags)
    tags = remove_URL(tags)
    return tags


for i in range(len(tags)):
    # print(type(tags[i]), i)
    if not isinstance(tags[i], str):
        tags[i] = 'None'
    tags[i] = remove_tags(tags[i])


## remove punctuations
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
porter = PorterStemmer()
corpus = []


## tokenize and stemming
for i in range(0,len(tags)):
    tokens = word_tokenize(tags[i])
    sw_tokens = [t for t in tokens if not t in stopwords.words('english')]
    pc_tokens = [t for t in sw_tokens if not t in punctuations]
    st_tokens = [porter.stem(t) for t in pc_tokens]
    corpus.append(st_tokens)


uni = ['university','uni','univerisities',
       'school','schools','college','colleges',
       'education','educate','educational']
uniwords = [porter.stem(w) for w in uni]


gov = ['governmental', 'government',
       'non-profit', 'charity']
govwords = [porter.stem(w) for w in gov]


start = ['innovative', 'innovation', 'innovations',
         'tech', 'technical', 'technology']
startwords = [porter.stem(w) for w in start]


num_cps = len(corpus)

flist = ['unclassified' for i in range(num_cps)]

for i in range(num_cps):
    cps = corpus[i]
    flist[i] = 'Mature Companies' if data['LAUNCH DATE'][i] < 1990 else 'unclassified'
    for uni in uniwords:
        if uni in cps:
            flist[i] = 'Universities/Schools'
            break
    for gov in govwords:
        if gov in cps:
            flist[i] = 'Government/Non-profit'
            break
    for start in startwords:
        if start in cps:
            flist[i] = 'Startups' if data['LAUNCH DATE'][i] >= 1990 else 'Mature Companies'


ftype = DataFrame(flist)
data['TYPE'] = ftype
DataFrame(data).to_excel('Data_Science_Internship_Assignment.xlsx', sheet_name='Data', index=False, header=True)






