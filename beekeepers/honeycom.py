import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from states import statesList
import os, sys, time
import pickle


def main():
    URL = 'https://honey.com/honey-locator'
    driver = webdriver.Chrome()
    driver.get(URL)
    masterDict = {}
    for state in statesList:

        print(state)
        # try:
        stateDf = pd.DataFrame()
        dropdown = Select(driver.find_element_by_xpath('/html/body/div[1]/main/div/div[3]/div[1]/div[1]/div[1]/select '))
        state = state.lower()
        dropdown.select_by_value(state)
        time.sleep(1)
        companies = driver.find_elements_by_class_name('item')
        for company in companies[:int(len(companies)/2)]:
            try:
                appendDict = {}
                compName = company.text.split('\n')[0].strip()
                generalLoc = company.text.split('\n')[-1].strip()
                time.sleep(.5)
                company.click()
                time.sleep(1)
                pars = driver.find_elements_by_class_name('paragraph')
                appendDict['company'] = compName
                appendDict['general_location'] = generalLoc
                for i, par in enumerate(pars):
                    appendDict[i] = par.text

                stateDf = stateDf.append(appendDict, ignore_index=True)
                time.sleep(1)
                driver.find_element_by_xpath('/html/body/div[1]/main/div/div[3]/div[2]/a').click()
                time.sleep(1)
            except:
                print(company.text, ' failed')
        masterDict[state] = stateDf



    try:
        with open('honeycom_dict.pickle', 'wb') as file:
            pickle.dump(masterDict, file)
    except:
        print('dict save failed')

    return masterDict


def postprocessing(data):
    master = pd.DataFrame(columns=['address', 'email', 'phone', 'description', 'rep', 'varietals', 'products', 'sizes' , 'markets' ,'orders' ,'company', 'location'])
    states = []
    for state, dat in data.items():

        for row in dat.iterrows():
            states.append(state)
            row = row[1]
            tempDict = {}
            for i, col in enumerate(dat.columns):
                tempDict[col] = dat.loc[i, col]

            master = master.append(tempDict, ignore_index=True)
    master['states'] = states

    master.to_csv('honeycomData.csv', index = False)


postprocessing(main())
