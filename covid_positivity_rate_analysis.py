# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:47:55 2020

@author: Tanay
"""
###Start analysis from 20th may
###End analysis on 6th Sept


import pandas as pd
import numpy as np
import datetime
from dateutil.parser import parse
import matplotlib.pyplot as plt

path = 'C:/Users/Tanay/Downloads'

testing = pd.read_csv(path+'/statewise_tested_numbers_data.csv')
confirmed = pd.read_csv(path+'/state_wise_daily.csv')
india_testing = pd.read_csv(path+'/tested_numbers_icmr_data.csv')
india_testing = india_testing.loc[:,["Tested As Of","Sample Reported today"]]
india_testing = india_testing.drop(42,axis=0)

testing_new = testing.iloc[:len(testing)-1,[0,1,5]]
st = "temp"
l = list()
for i,r in testing_new.iterrows():
    #if(r["State"]!=st):
    #    l.append(r["Total Tested"])
    if(np.isnan(testing_new.iloc[i,2])):
        testing_new.iloc[i,2] = testing_new.iloc[i-1,2]

for i,r in testing_new.iterrows():
    if(r["State"]!=st):
        l.append(r["Total Tested"])
    else:
        l.append(testing_new.iloc[i,2] - testing_new.iloc[i-1,2])
    st = r["State"]

datelist = list()
for i,r in testing_new.iterrows():
    dt = parse(r['Updated On'])
    datelist.append(dt.date())
    
testing_new.insert(2,"Daily Tested",l)
testing_new.insert(2,"Good Dates",datelist)
ncidx = [i for i in range(534) if(i%3!=0)]
confirmed_new = confirmed.drop(ncidx)
total = list()
confirmed_new = confirmed_new.drop(labels=["UN"],axis=1)

cdatelist = list()
for i,r in confirmed_new.iterrows():
    dt = parse(r['Date'])
    cdatelist.append(dt.date())
    
confirmed_new.insert(2,"Good Dates",cdatelist)

idatelist= list()
for i,r in india_testing.iterrows():
    x =list(map(int,r['Tested As Of'].split("/")))
    #print(x)
    idatelist.append(datetime.date(x[2],x[1],x[0]))
india_testing.insert(2,"Good Dates",idatelist)

confirmedtuplist = list()
for i,r in confirmed_new.iterrows():
    if(r["Good Dates"]>datetime.date(2020,5,19) and r["Good Dates"]<=datetime.date(2020,9,6)):
        confirmedtuplist.append((r["Good Dates"],r["TT"]))

testingtuplist = list()
for it,rn in india_testing.iterrows():
    if(rn["Good Dates"]>datetime.date(2020,5,19) and rn["Good Dates"]<=datetime.date(2020,9,6)):
        testingtuplist.append((r["Good Dates"],int(rn["Sample Reported today"])))

positiverate = list()
plotdatelist = list()
for k in zip(confirmedtuplist,testingtuplist):
    positiverate.append(100*k[0][1]/k[1][1])
    plotdatelist.append(k[0][0])

plt.plot(plotdatelist,positiverate)
plt.plot(plotdatelist,[8.5]*len(plotdatelist))
plt.title('Positive Rate Trend from 20-May to 6-Sept for India')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.ylabel('Rate')
plt.show()