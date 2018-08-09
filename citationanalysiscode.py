#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 10:36:49 2018

@author: hk
"""

import os
os.getcwd()
os.chdir('/Users/hk/Dropbox/TDI/Project')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def hIndex(citations):
    h = 0
    for x in citations:
        if x >= h + 1:
            h += 1
        else:
            break
    return h

#reading in files
gp = pd.read_csv('gnum2000-2.csv')
cp = pd.read_csv('gnum2000-0.csv')

#making column names consistent
gp = gp.rename(columns={"pmids": "pid"})

#merging data
data = gp.merge(cp, how = 'left', on = 'pid')
data2 = data.sort_values(['gid', 'cites'], ascending=[True, False])
data2 = data.set_index('gid')
del data2['pid']

data3 = data2.groupby('gid').agg(['sum', 'mean', 'min', 'max', 'median'])
data3.columns = data3.columns.droplevel(0)
data3.head()



#calculating h index
#making lists to put in h index function
clist = data2.groupby('gid')['cites'].apply(list)
#calling hindex function over lists
hindex = []
for l in clist:
    hindex.append(hIndex(l))

#adding h index to dataset
data3['hindex'] = hindex
data3.reset_index(level=0, inplace=True)
data3.head()

#saving dataset as a file:
data3.to_csv('allanalysis2000.csv', sep = ',', index = True)

#loading raw data from NIH
df = pd.read_csv('RePORTER_PRJ_C_FY2000.csv')

#parsing out grant id numbers
df['gnum'] = df['CORE_PROJECT_NUM'].str[3:]

#converting enddate to datetime
df['enddate'] = pd.to_datetime(df['BUDGET_END'])

#pulling specific columns from the raw data
rawgrantdata = pd.DataFrame({'gid' : df['gnum'],
                        'mech' : df['ACTIVITY'],
                        'center' : df['ADMINISTERING_IC'],
                        'centername' : df['IC_NAME'],
                        'enddate': df['enddate']})

#removing duplicates from the data
rawdata = rawgrantdata.drop_duplicates(subset = 'gid', keep = 'first')

#mergiing with calculated values
adata1 = data3.merge(rawdata, how = 'left', on = 'gid')

#removing missing values:
import numpy as np
adata2 = adata1.replace('', np.nan, inplace=False)
adata2.dropna(inplace=True)

adata2.to_csv('allanalysis2000_nomiss.csv', sep = ',', index = False)
adata2['year'] = adata2['enddate'].dt.strftime('%Y')


#frequencies:
#adata2.crosstab('mech', 'center')
print(adata2['mech'].value_counts())
print(adata2['center'].value_counts())

#subsetting to National Cancer Insititute
CAdata = adata2[adata2['center'] == 'CA']
GMdata = adata2[adata2['center'] == 'GM']
HLdata = adata2[adata2['center'] == 'HL']

top3 = top3.append(GMdata)

print(CAdata['year'].value_counts())

keep = []
for x in adata2['mech']:
    if x in ('R01', 'T32', 'R29', 'F32', 'K08'):
        keep.append(1)
    else:
        keep.append(0)

adata2['keep'] = keep

top5 = adata2[adata2['keep']==1]

catop5 = top35[top35['center']=='CA']


my_tab = pd.crosstab(index=top35["center"],  # Make a crosstab
                              columns="mech")
#my_tab.index = ['CA', 'GM', 'HL']
my_tab.columns = ['R01', 'T32', 'R29', 'F32', 'K08']
my_tab


#plotting
x = [pd.to_datetime(d) for d in catop5['enddate']]
y = catop5['hindex']
cgroup = top35['center']
mgroup = catop5['mech']
ccolors = {'HL':'red', 'GM':'blue', 'CA':'green'}
mcolors = {'R01':'red', 'T32':'blue', 'R29':'green', 'F32': 'yellow', 'K08': 'black'}

plt.scatter(x, y, c=mgroup.apply(lambda x: mcolors[x]), alpha = 0.5)
plt.show()


gtop5 = top5.groupby(top5['mech']).agg(['mean', np.std])


data = pd.read_csv('allanalysis2000.csv')
