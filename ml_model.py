#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 18:03:51 2018

@author: hk
"""

#### DIRECTORY
import os
os.getcwd()
os.chdir('/Users/hk/Dropbox/TDI/Project')

#### LIBRARIES
import pandas as pd
#import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression

### FILES

#raw data from NIH
df00 = pd.read_csv('RePORTER_PRJ_C_FY2000.csv')
df10 = pd.read_csv('RePORTER_PRJ_C_FY2010.csv')

#Y2000 grant calculated variable file
grantdata = pd.read_csv('allanalysis2000_nomiss.csv', header = 0)

### FUNCTIONS


### DATA CLEANING/WRANGLING & VARIABLE CALCULATIONS

#renaming columns
df00.rename(columns={'PI_NAMEs':'pi'}, inplace=True)
df00.rename(columns={'ORG_NAME':'org'}, inplace=True)
df10.rename(columns={'PI_NAMEs':'pi'}, inplace=True)

#parsing out grant id numbers
df00['gid'] = df00['CORE_PROJECT_NUM'].str[3:]

#creating new dataset of just Y2000 gids and PIs
pi00= pd.DataFrame({'gid': df00['gid'], 'pi': df00['pi']})

#merging pi dataset with grant data
pigrants00 = pd.merge(pi00, grantdata, on=['gid', 'gid'])
#pigrants00.head()

#assessing frequency of pis on grants
pigrants00['pi'].value_counts()

#calculating values over PIs
funcs = {'sum':['sum','mean'], 'mean':['mean'], 'min':['min'],
         'max':['max'], 'median':['median'], 'hindex':['mean', 'count']}

pis00 = pigrants00.groupby('pi').agg(funcs)
pis00.columns = pis00.columns.droplevel(0)
pis00.columns = ['sum', 'sum_mean', 'mean', 'min', 'max', 'median', 'h_mean', 'count']

#deleting empty PI name
pi00 = pis00[pis00.index != ',;']

#making lists of pi names to compare
pi10_list = [pi for pi in df10['pi'] if pi != ',;'] #Y2010 list
pi10_list = set(pi10_list)

#creating loop of Y/N if Pi has active grant in 2010
grant2010 = []
for pi in pi00.index:
    if pi in pi10_list: grant2010.append(1)
    else: grant2010.append(0)


#Logistic model:
#X = pi00
#y = grant2010

logreg = LogisticRegression()

#whole dataset as a predictor
logreg.fit(pi00, grant2010)
logreg.score(pi00, grant2010)
#R^2: 0.65764441831881582
logreg.coef_
    #seems count, median, mean, and h-index


#Just count as a predictor
logreg.fit(pi00[['count']], grant2010)
logreg.score(pi00[['count']], grant2010)
#R^2: 0.61828675252498266
logreg.coef_


#Creating University Rank System (Top 125)

#Getting list of nonrepeated organizatio names
univ = df00.groupby('org').agg('count')
uni = univ.index

#Creating column of placeholders to input average college rank
df00['averank'] = [0]*83500

#Finding organization with a given name
matching = [s for s in uni if "ARIZONA STATE U" in str(s) and not " OH" in str(s)]
matching #list of orgs

#loop to reassign average org rank value
for value in df00['org']:
    if value in matching:
        df00.loc[df00['org'] == value, 'averank'] = 131.375

#df00.to_csv('df00.csv', sep = ',', index = True)

#creating new dataset of just Y2000 gids and PIs
pior00= pd.DataFrame({'gid': df00['gid'], 'pi': df00['pi'],
                    'averank': df00['averank']})

#merging pi dataset with grant data
piorgrants00 = pd.merge(pior00, grantdata, on=['gid', 'gid'])
#pigrants00.head()

#assessing frequency of pis on grants
piorgrants00['pi'].value_counts()

#calculating values over PIs
funcs2 = {'averank': ['mean'], 'sum':['sum','mean'], 'mean':['mean'], 'min':['min'],
         'max':['max'], 'median':['median'], 'hindex':['mean', 'count']}

pisor00 = piorgrants00.groupby('pi').agg(funcs2)
pisor00.columns = pisor00.columns.droplevel(0)
pisor00.columns = ['averank', 'sum', 'sum_mean', 'mean', 'min', 'max', 'median', 'h_mean', 'count']

#deleting empty PI name
piar00 = pisor00[pisor00.index != ',;']
#deleting emptly average org rank
piar00 = piar00[piar00['averank'] != 0]

averank = list(piar00['averank'])
piar00_2 = piar00.drop(['averank'], axis=1)

#modeling
linreg = LinearRegression()

#whole dataset as a predictor
linreg.fit(piar00_2, averank)
linreg.score(piar00_2, averank)
#R^2: 0.044627044823447481
linreg.coef_ #coef are negative as expected but not large.


#making lists of pi names to compare
pi10_list = [pi for pi in df10['pi'] if pi != ',;'] #Y2010 list
pi10_list = set(pi10_list)

#creating loop of Y/N if Pi has active grant in 2010
grant2010 = []
for pi in piar00_2.index:
    if pi in pi10_list: grant2010.append(1)
    else: grant2010.append(0)

#mean citations dataset as a predictor
logreg.fit(piar00, grant2010)
logreg.score(piar00, grant2010)
#R^2: 0.65582004804542482
logreg.coef_
#

