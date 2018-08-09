#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 10:28:31 2018

@author: hk
"""

import os
os.getcwd()
os.chdir('/Users/hk/Dropbox/TDI/Project')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('RePORTER_PRJ_C_FY2000.csv')
data = pd.read_csv('allanalysis2000_nomiss.csv')
df['gid'] = df['CORE_PROJECT_NUM'].str[3:]

adata1 = df.merge(data, how = 'left', on = 'gid')

udata1 = pd.DataFrame({'gid' : adata1['gid'],
                       'mech' : adata1['mech'],
                        'org' : adata1['ORG_NAME'],
                        'sum' : adata1['sum'],
                        'mean' : adata1['sum'],
                        'min' : adata1['min'],
                        'max' : adata1['max'],
                        'median' : adata1['median'],
                        'hindex' : adata1['hindex']})



udata2 = udata1.groupby('org').agg(['mean', 'median'])
udata2.columns = udata2.columns.droplevel(0)
udata2.columns = ['sum_mean', 'sum_median', 'mean_mean', 'mean_median',
                  'min_mean', 'min_median', 'max_mean', 'max_median',
                  'median_mean', 'median_median', 'hi_mean', 'hi_median']
udata2.head()
udata3 = udata2.dropna(axis=0)

udata3.reset_index(level=0, inplace=True)

udata3.to_csv('udata3.csv', sep = ',', index = False)

subus = ['Harvard', 'Princeton', 'Yale', 'Emory',  'Georgetown']
ukeep = []
for elem in udata3['org']:
    k = 0
    for u in subus:
        if u in elem: k = 1
    ukeep.append(k)
len(ukeep)



udesc = pd.DataFrame({'centername' : adata1['IC_NAME'],
                        'city' : adata1['ORG_CITY'],
                        'state' : adata1['ORG_STATE'],
                        'org' : adata1['ORG_NAME']})




mdata1 = pd.DataFrame({'mech' : adata1['mech'],
                        'sum' : adata1['sum'],
                        'mean' : adata1['sum'],
                        'min' : adata1['min'],
                        'max' : adata1['max'],
                        'median' : adata1['median'],
                        'hindex' : adata1['hindex']})
mdata1 = mdata1.dropna(axis=0)

mdata2 = mdata1.groupby('mech').agg(['mean', 'median'])
mdata2.columns = mdata2.columns.droplevel(0)
mdata2.columns = ['hi_mean', 'hi_median', 'max_mean', 'max_median',
                  'mean_mean', 'mean_median', 'median_mean', 'median_median',
                  'min_mean', 'min_median', 'sum_mean', 'sum_median']



mdata2.reset_index(level=0, inplace=True) #resetting index and making old values a column

mcounts = mdata1['mech'].value_counts()
mcountsid = mdata1['mech'].value_counts().index.tolist()
print(mcounts)
mcdata = pd.DataFrame({'mcount':mcounts, 'mech':mcountsid})


mdata3 = mdata2.merge(mcdata, how = 'left', on = 'mech')
mdata3 = mdata3.sort_values('mcount', ascending=False)
mdata3.head()

mdata3_norm = pd.DataFrame({'hi_mean': mdata3['hi_mean']/mdata3['mcount'],
                            'mean_mean': mdata3['mean_mean']/mdata3['mcount'],
                            'median_mean': mdata3['median_mean']/mdata3['mcount']})

mechgraphall = mdata4[0:4]
mechgraphall.set_index(mechgraphall['mech'])
#'hi': mechgraphall['hi_mean'],
graph1 = pd.DataFrame({'mean': mechgraphall['mean_mean'],
                       'median': mechgraphall['median_mean'],
                       'hindex': mechgraphall['hi_mean'],
                       'mech' : mechgraphall['mech']})
graph1.set_index('mech')

ax = graph1.plot.bar(rot=0)


import matplotlib.pyplot as plt
import matplotlib.lines as mlines
#from matplotlib.dates import date2num
#import datetime

x = graph1['mech']
xd = ['Large Independent Research', 'Center Training','Early Career Research',
      'Postdoctoral Research']
y1 = graph1['median']
y2 = graph1['hindex']

#Median Figure
ax1 = plt.subplot(1,1,1)
plt.title('Median Citations by Top Grant Mechanisms')
#plt.xlabel('Grant Mechanisms')
plt.ylabel('Average Median Citations')
plt.xticks(rotation=45, ha = 'right')
ax1.bar(xd, y1, color = 'r', width=0.5)
plt.savefig('/Users/hk/Dropbox/TDI/Project/Project Presentations/medianfig.png', dpi=None, facecolor='w', edgecolor='w')
plt.show()

#HIndex Figure
ax2 = plt.subplot(1,1,1)
plt.title('H-Index by Top Grant Mechanisms')
#plt.xlabel('Grant Mechanisms')
plt.ylabel('Average H-Index')
plt.xticks(rotation=45, ha = 'right')
ax2.bar(xd, y2, color = 'b', width=0.5)
plt.savefig('/Users/hk/Dropbox/TDI/Project/Project Presentations/hindexfig.png', dpi=None, facecolor='w', edgecolor='w')
plt.show()


#University scatter

rankdata = pd.read_csv('Urankdata.csv')
y3 = rankdata['mean_mean']
x2 = rankdata['rank']

ax3 = plt.subplot(1,1,1)
plt.title('Mean Citations per Grant by University Rank')
plt.ylabel('Average Mean Citations')
plt.xlabel('Rankings (1 is Best)')
ax3.scatter(x2, y3, color = 'g')
line = mlines.Line2D([0, 101], [250, 58], color='orange')
ax3.add_line(line)
#for i, txt in enumerate(rankdata['org']):
#    ax3.annotate(txt, (x2[i],y3[i]))

plt.show()

y4 = rankdata['median_mean']

ax4 = plt.subplot(1,1,1)
plt.title('Median Citations per Grant by University Rank')
plt.ylabel('Average Median Citations')
plt.xlabel('Rankings (1 is Best)')
ax4.scatter(x2, y4, color = 'orange')
line = mlines.Line2D([0, 101], [1.8, 1.8], color='green')
ax4.add_line(line)
#for i, txt in enumerate(rankdata['org']):
#    ax4.annotate(txt, (x2[i],y4[i]))

plt.show()


