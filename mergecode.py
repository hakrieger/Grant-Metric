#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 20:04:13 2018

@author: hk
"""

import os
os.getcwd()
os.chdir('/Users/hk/Dropbox/TDI/Project')
import pandas as pd
import numpy as np

#importing NIH dataset
df = pd.read_csv('RePORTER_PRJ_C_FY2000.csv')

#parsing out grant id numbers
df['gnum'] = df['CORE_PROJECT_NUM'].str[3:] #parsing to get just the grant num
#df['mech'] = df['CORE_PROJECT_NUM'].str[0:3] #parsing the mechanism

rawgrantdata = pd.DataFrame({'gid' : df['gnum'],
                        'mech' : df['ACTIVITY'],
                        'center' : df['ADMINISTERING_IC'],
                        'centername' : df['IC_NAME'],
                        'city' : df['ORG_CITY'],
                        'state' : df['ORG_STATE'],
                        'org' : df['ORG_NAME'],
                        'dept' : df['ORG_DEPT'],
                        'district' : df['ORG_DISTRICT'],
                        'cost' : df['TOTAL_COST']})
rawgrantdata.set_index(rawgrantdata['gid'])

pidata = pd.DataFrame({'gid' : df['gnum'],
                        'mech' : df['ACTIVITY'],
                        'pid' : df['PI_IDS'],
                        #'name' : df['NAME']
                        })


cites = pd.read_csv('gnum2000-1.csv')
cites.set_index(cites['gid'])

grantdata = pd.concat([cites, rawgrantdata], axis=1, join='inner')

grantdata.to_csv('allgrants2000.csv', sep = ',', index = True)


df['enddate'] = pd.to_datetime(df['BUDGET_END'])
ended = df.set_index(df['enddate'])
ended = ended.loc['2006-12-31':'2008-01-01']

#outputing ended as a file
ended.to_csv('ended2007.csv', sep = ',', index = True)



#removing duplicate grant ID numbers
gnum = np.unique(np.array(ended.gnum))
len(gnum)
