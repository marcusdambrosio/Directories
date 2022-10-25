import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os, sys, time
import pickle


URL = 'http://www.bees-on-the-net.com/?page_id=1187'
def main():
    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(1)
    pre='menu-item menu-item-type-post_type menu-item-object-page menu-item-'
    pre="menu-item-"

    stateClasses = [pre + str(n) for n in range(1347, 1399)]
    hrefs = []
    for c in stateClasses:
        block = driver.find_element_by_id(c)
        tag = block.find_element_by_tag_name('a')
        hrefs.append(tag.get_attribute('href'))
    data = []
    for h in hrefs:
        print(h)
        driver.get(h)
        time.sleep(1)
        sList = driver.find_elements_by_class_name('swarmList')
        if type(sList) == list:
            for s in sList:
                data.append(s.text)
        else:
            data.append(sList.text)

    with open('savelist.txt', 'wb') as fp:
        pickle.dump(data, fp)

def processing():
    states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
              'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
              'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
              'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
              'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    master = pd.DataFrame(columns=['name', 'state', 'website', 'phone', 'email', 'company', 'notes'])
    splitVar='__________________________________________________'
    with open('savelist.txt','rb') as fp:
        saveList = pickle.load(fp)
    for l in saveList:
        comps = l.split(splitVar)
        for state in states:
            if state in comps[1]:
                currState = state
                break
        for c in comps:
            cSplit = c.split('\n')
            if cSplit == ['']:
                continue
            name = cSplit[1]
            descr = cSplit[-2]
            phone = ''
            company = ''
            email = ''
            website = ''
            for dat in cSplit:
                if ':' in dat:
                    try:
                        if 'URL' in dat or 'Website' in dat or 'Web Site' in dat:
                            website = dat.strip('URL:').strip()
                        elif 'phone' in dat.lower() or 'cell' in dat.lower():
                            phone = dat.split(':')[-1].strip() + ' '
                            cat, num = [x.strip() for x in dat.split(':')]
                        elif 'mail' in dat.lower():
                            email = dat.split(':')[-1].strip()
                        elif 'company' in dat.lower():
                            company = dat.split(':').strip()
                    except:
                        print(dat.split(':'))
            master=master.append({'name':name,
                                  'phone':phone,
                                  'email':email,
                                  'company':company,
                                  'website':website,
                                  'notes':descr,
                                  'state': currState}, ignore_index=True)
    master.to_excel('master_list.xlsx', index = False)


if __name__ == '__main__':
    processing()
