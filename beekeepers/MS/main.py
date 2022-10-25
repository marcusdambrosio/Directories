import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os, sys, time
import pickle
from selenium.webdriver.chrome.options import Options
import json
import re

URL = 'https://mshoneybee.org/bee-producers/'


def pull():
    driver = webdriver.Chrome()
    driver.get(URL)

    masterTxt = ''
    ele = driver.find_element_by_xpath('/html/body/div[1]/div[2]/main/div/section/div/div/div[3]/div/div')
    pars = ele.find_elements_by_tag_name('p')
    master = []
    for p in pars[1:-1]:
        master.append(p.text)
    txt = ele.text
    # for i in [3,4,5,6]:
    #     ele = driver.find_element_by_class_name(f'fusion-text fusion-text-{i}')
    #     txt = ele.text + '\n\n BREAK \n\n'
    #

    with open('MS_text.txt', 'wb') as f:
        pickle.dump(master,f)



def process():
    with open('MS_text.txt', 'rb') as f:
        txt = pickle.load(f)
    master = pd.DataFrame(columns = ['name', 'phone', 'email'])
    for t in txt:
        name = ''
        phone = ''
        email = ''
        for line in t.split('\n'):
            if line == '':
                continue
            if line == t.split('\n')[0]:
                name = line.strip()
            if len(re.sub('[^0-9]', '', line)) >8:
                phone = re.sub('[^0-9]', '', line)
            if '@' in line:
                email = line.strip()
        master = master.append({'name':name,
                                'phone':phone,
                                'email':email}, ignore_index=True)

    master.to_excel('mississippie_beekeepers.xlsx', index=  False)

    master.to_csv('mississippie_beekeepers.csv', index=  False)
    return


if __name__ == '__main__':
    process()


