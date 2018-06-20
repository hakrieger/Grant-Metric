# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 10:53:37 2017

@author: hkrieger
"""
import os
os.getcwd()


"""
Using Grant Numbers to get PMIDS of published papers
"""

import requests, time
from bs4 import BeautifulSoup as bs

gpubc = open('gpubcount2.txt', 'w')
gpubids = open('gpubids2.txt','w')
fpmids = open('pmidsonly2.txt','w')

pcount = []
grant = []
apmid = []

start = time.time()
loopnum = 1

urlmain1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=1000&term="
urltail1 = "[Grant%1000Number]"
for number1 in ["AA014576",'AA024377']:
    url1 = urlmain1+str(number1)+urltail1

    page1 = requests.get(url1)
    soup1 = bs(page1.content, 'html.parser')

    pubcount = soup1.find('count')
    pubc = pubcount.get_text()
    pcount.append(pubc)
    grant.append(number1)

    pmids = soup1.find_all('id')
    idarray = []
    #gnum = []

    for idnum in pmids:
      idarray.append(idnum.get_text())
    m=0

    while m <= (len(idarray)-1):
        gpubids.write(str(number1)+' '+str(idarray[m])+'\n')
        fpmids.write(str(idarray[m])+'\n')
        print(time.time(),number1,idarray[m])
        m=m+1

    if(loopnum <= 10):  #restricting the number of requests to 10
        loopnum = loopnum +1
    else:
        diff = (time.time()-start)
        time.sleep(1-diff)      #forcing a pause for only 10 requests a second
        start = time.time()
        loopnum = 1


n=0
while n <= (len(grant)-1):
    gpubc.write(str(n+1)+' '+str(grant[n])+' '+str(pcount[n])+'\n')
    #print(n+1,grant[n],pcount[n])
    n=n+1

gpubc.close()
gpubids.close()
fpmids.close()


"""
Using PMIDS to get cited by counts
"""
#fpmids2 = open('fpmids1.txt','r') #pmidsonly.txt
#for line in fpmids2:
#    number2.append(line.strip('\n'))

import time

urlmain2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pmc_refs&id="

citecount = open('citecount.txt', 'w')
pubid = []
cites = []

start = time.time()
loopnum = 1

for number in [29097835, 28580226, 28548347, 27588833, 27260007, 27030295, 29226004, 29097835, 28772247, 28580226]:
    url = urlmain2+str(number)
    page2 = requests.get(url)
    soup2 = bs(page2.content, 'html.parser')
    ids = soup2.find_all('id')
    aid = ids[0].get_text()
    count = len(ids)-1
    aidr=str(aid)
    countr=str(count)
    pubid.append(aidr)
    cites.append(countr)


    if(loopnum <= 10):  #restricting the number of requests to 10
        loopnum = loopnum +1
    else:
        diff = (time.time()-start)
        time.sleep(1-diff)      #forcing a pause for only 10 requests a second
        start = time.time()
        loopnum = 1


m=0
while m <= (len(pubid)-1):
    citecount.write(str(m+1)+' '+str(pubid[m])+' '+str(cites[m])+'\n')
    print(m+1,time.asctime( time.localtime(time.time()) ),pubid[m],cites[m])
    m=m+1

citecount.close()






