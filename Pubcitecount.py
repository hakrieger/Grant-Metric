#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 17:42:03 2018

@author: hk
"""

"""
Using PMIDS to get cited by counts
"""

import os
os.chdir('/Users/hk/Dropbox/TDI/Project')

import time, requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

#creating functions to work with scrapped NCBI output
class ncbi:
    def __init__(self):
        self.items = []

    #defining concatination tool
    def concat_ids(a):
        result= ''
        for element in a: result += "&id=%s" %(element)
        return result

    #creating 200 id endings to put on urls for pull request
    def urlends(a):
        count = (len(a)//200)
        ends = []
        n = 0
        while n <= count:
            idstr = ncbi.concat_ids(a[0+(n*200):200+(n*200)])
            ends.append(idstr)
            n = n + 1
        return ends

#importing in file
aids = pd.read_csv('gnum2001-2.csv')
#len(aids.pmids)
aids_nz = sorted(aids.pmids[aids.pmids != 0]) #removing PMIDS of 0
aidsu = np.array(aids_nz)
aidsu = list(np.unique(aids_nz))#removing duplicate article pmids
len(aidsu) #identifying length of pmids to pull info for


#identifying number of 200 pmid batches
count = (len(aidsu)//200)
count

#assigning url to pull from
urlmain2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pmc_refs&email=heather.a.krieger@gmail.com"
apikey = "&api_key=87d16f20bd554d28372d7d9e4003ea03d508"

#making urlends:
urlend = ncbi.urlends(aidsu)

#loop through created urls to scrap data from ncbi
start = time.time()
carray = []
n = 0
while n < len(urlend):
    url = urlmain2+apikey+urlend[n]
    page2 = requests.get(url)
    soup2 = bs(page2.content, 'html.parser')
    a = soup2.findAll('linkset')
    i = 0
    while i < len(a):
        b = a[i].findChildren('id')
        carray.append(len(b)-1)
        i = i+1
    n = n+1

end = time.time()
diff = end-start
print(diff)

citecounts = pd.DataFrame({'pid' : aidsu,
                       'cites' : pd.Series(carray)})
citecounts.to_csv('gnum2001-0.csv', sep = ',', index = False)





