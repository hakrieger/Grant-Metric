#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Using Grant Numbers to get PMIDS of published papers

Created on Thu Apr  5 15:05:23 2018

@author: hk
"""
import os
os.getcwd()
os.chdir('/Users/hk/Dropbox/TDI/Project')

import requests, time
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np


#importing NIH datafile
df = pd.read_csv('RePORTER_PRJ_C_FY2007.csv')

#restricting to projecting ending in the year the data was downloaded:
df['enddate'] = pd.to_datetime(df['BUDGET_END'])
ended = df.set_index(df['enddate'])
ended = ended.loc['2006-12-31':'2008-01-01']

#outputing ended as a file
ended.to_csv('ended2007.csv', sep = ',', index = True)

ended['gnum'] = ended['CORE_PROJECT_NUM'].str[3:] #parsing to get just the grant num
ended['mech'] = ended['CORE_PROJECT_NUM'].str[0:3] #parsing the mechanism

#removing duplicate grant ID numbers
gnum = np.unique(np.array(ended.gnum))
len(gnum)

#assigning url information
urlmain1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=5000&email=heather.a.krieger@gmail.com&term="
urltail1 = "[Grant%1000Number]&api_key="
apikey = "87d16f20bd554d28372d7d9e4003ea03d508"

#creating empty lists to append gathered data to
pcount = []
idarray = []
gnarray = []

#loop to collect data
j=0
start = time.time()
while j < len(gnum):

    url1 = urlmain1+gnum[j]+urltail1+apikey
    page1 = requests.get(url1)
    soup1 = bs(page1.content, 'html.parser')

    try:
        pubcount = soup1.find('count')
        pubc = pubcount.get_text()
        pcount.append(pubc)
    except:
        pcount.append('0')


    try:
        pmids = soup1.find_all('id')
        idar = []
        if pmids != []:
            for idnum in pmids:
                idar.append(idnum.get_text())
                gnarray.append(gnum[j])
            idarray = idarray + idar
        else:
            idarray.append('0')
            gnarray.append(gnum[j])
    except:
        idarray.append('0')
        gnarray.append(gnum[j])
    j = j+1

end = time.time()
diff = end-start
print(diff)

#saving grant numbers and the number of publications they are listed on
pubcounts = pd.DataFrame({'gid' : gnum, 'pubcount' : pd.Series(pcount)})
pubcounts.to_csv('pubcount2000.csv', sep = ',', index = False)

#saving long list of pmids to use for getting citation counts
pmidsforcites = pd.DataFrame({'gid' : pd.Series(gnarray), 'pmids' : pd.Series(idarray)})
pmidsforcites.to_csv('pmids2000.csv', sep = ',', index= False)
