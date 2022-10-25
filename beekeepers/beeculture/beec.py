import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os, sys, time
import pickle
import re

def main():
    URL = 'https://www.beeculture.com/find-local-beekeeper/'
    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(1)
    states = driver.find_elements_by_class_name('homeTopLinks')
    states=states[:-4]

    canada = ['Alberta','British Columbia','Manitoba','New Brunswick',
                'Nova Scotia','Ontario','Prince Edward Island','Quebec','Saskatchewan']
    stateAbbr = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                 "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                 "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                 "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                 "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    for s in states:
        if s.text in canada:
            states.remove(s)
    stateNames=[s.text for s in states]
    master = pd.DataFrame()
    compHolder = []
    for i, state in enumerate(states):
        newStates = driver.find_elements_by_class_name('homeTopLinks')
        for s in newStates:
            if s.text in canada:
                newStates.remove(s)
        newStates[i].click()
        time.sleep(1)

        comps = [c.text for c in driver.find_elements_by_class_name('homeTopLinks')]
        newComps = []
        for comp in comps:
            if len(comp.split('\n'))>2:
                newComps.append(comp)

        for comp in newComps:
            compHolder.append([stateNames[i], comp])

        # for comp in comps:
        #     master = master.append({'state':stateNames[i],
        #                             'data':comp}, ignore_index=True)
        driver.get(URL)
        time.sleep(1)
    # master.to_csv('dataDf.csv',index=False)
    new = pd.DataFrame(columns=['state', 'company','name', 'title', 'address', 'phone1', 'phone2', 'email1', 'email2', 'website', 'facebook'])
    fails = []
    # for row in master.iterrows():

    for row in compHolder:
        # i,row = row
        add = ''
        phones=[]
        emails=[]
        web, fb = None, None
        # state,data = row['state'], row['data']
        state,data=row[0].strip(), row[1]

        # try:
        dat = [d.strip() for d in data.split('\n')]
        print(dat)
        try:
            dat.remove('')
        except:
            pass
        try:
            dat.remove(' ')
        except:
            pass

        company = dat[0]
        foundPhone=False
        for n in range(len(dat)):
            if ('phone' in dat[n].lower() or 'email' in dat[n].lower()) and not foundPhone:
                if 'phone' in dat[n].lower():
                    if not len(phones):
                        phones = [dat[n].split(':')[-1].strip()]
                    else:
                        phones.append(dat[n].split(':')[-1].strip())
                elif 'email' in dat[n].lower():
                    if not len(emails):
                        emails=[dat[n].split(':')[-1].strip()]
                    else:
                        emails.append(dat[n].split(':')[-1].strip())
                foundPhone=True
                frontDat = dat[:n]
                nameTitle=[]
                allAdd = []
                for fd in frontDat[1:]:
                    noState=False
                    if re.sub('[^0-9]','',fd) == '':
                        for stAbb in stateAbbr:
                            if stAbb not in fd:
                                noState=True
                            else:
                                noState=False
                                allAdd.append(fd)
                                break
                        if noState:
                            nameTitle.append(fd)
                    else:
                        allAdd.append(fd)
            else:
                if 'phone' in dat[n].lower():
                    if not len(phones):
                        phones = [dat[n].split(':')[-1].strip()]
                    else:
                        phones.append(dat[n].split(':')[-1].strip())
                elif 'email' in dat[n].lower():
                    if not len(emails):
                        emails=[dat[n].split(':')[-1].strip()]
                    else:
                        emails.append(dat[n].split(':')[-1].strip())
                elif 'website' in dat[n].lower():
                    web = dat[n].split(':')[-1].strip()
                elif 'facebook' in dat[n].lower():
                    fb = dat[n].split(':')[-1].strip()
        add = ''
        for a in allAdd:
            if a ==allAdd[0]:
                add=a
            else:
                add=add+', '+a.strip()

        if len(nameTitle)>1:
            name=nameTitle[0]
            title=nameTitle[1]
        elif len(nameTitle)==1:
            name=nameTitle[0]
            title=None
        else:
            name = None
            title = None

        if len(phones)>1:
            phone1 = phones[0]
            phone2 = phones[1]
        elif len(phones) == 1:
            phone1 = phones[0]
            phone2=None
        else:
            phone1=None
            phone2=None

        if len(emails)>1:
            email1 = emails[0]
            email2 = emails[1]
            if len(emails)>2:
                print(emails)
        elif len(emails)==1:
            email1 = emails[0]
            email2=None
        else:
            email1=None
            email2=None

        new=new.append({'state':state,
                        'company':company,
                        'name':name,
                        'title':title,
                        'address':add,
                        'phone1':phone1,
                        'phone2':phone2,
                        'email1':email1,
                        'email2':email2,
                        'website':web,
                        'facebook':fb}, ignore_index=True)

    new.to_csv('beeculture_masterNEW.csv', index=False)


        # except Exception as e:
            # print(e)
            # sys.exit()
            # title, add,phone,email1, email2,web,fb = 0,0,0,0,0,0,0
            # company = dat
            # name = e
            # fails.append(i)
            # new=new.append({'state':state,
            #                 'company':company,
            #                 'name':name,
            #                 'address':add,
            #                 'phone':phone,
            #                 'email1':email1,
            #                 'email2':email2,
            #                 'wesbite':web,
            #                 'facebook':fb}, ignore_index=True)





main()