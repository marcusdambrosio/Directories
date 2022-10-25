import os,sys,time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


def nevada_grown():
    url = 'https://nevadagrown.com/farmers/'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    comps = driver.find_elements_by_class_name('pt-cv-ifield')
    time.sleep(1)
    names = [c.text for c in comps]
    comps = [c.find_element_by_tag_name('a') for c in comps]
    hrefs = [c.get_attribute('href') for c in comps]
    master = pd.DataFrame()
    for i, comp in enumerate(comps):
        print(f'{names[i]} started. \n')
        driver.get(hrefs[i])
        time.sleep(3)
        try:
            try:
                desc = driver.find_element_by_class_name('fusion-text').text.strip()
            except:
                desc = 'None'
                print('description failed')
            # print(desc)
            compInfo = driver.find_element_by_class_name('company_info').text
            try:
                add = compInfo.split('\n')[1].strip()
            except:
                add = 'None'
                print('address failed')
            # print(add)
            try:
                website = driver.find_element_by_class_name('i_website').find_element_by_tag_name('a').get_attribute('href').strip()
            except:
                website = 'None'
                print('website failed')
            # print(website)

            try:
                email = driver.find_element_by_class_name('popup').get_attribute('href')
                email = email.split('address=')[-1].strip()
            except:
                email = 'None'
                print('email failed')
            # print(email)
            try:
                phone = [p for p in compInfo.split('\n') if 'Phone' in p][0].split(':')[-1].strip()
            except:
                phone = 'None'
                print('phone failed')
            # print(phone)
            try:
                products = driver.find_element_by_class_name('tags').text.strip()
            except:
                products = 'None'
                print('products failed')
            # print(products)
            master = master.append({'company': names[i],
                                    'description' : desc,
                                    'address' : add,
                                    'website': website,
                                    'email' : email,
                                    'phone': phone,
                                    'products': products}, ignore_index=True)
            driver.back()
            time.sleep(1)
        except:
            print(names[i], ' failed')
            driver.back()
            time.sleep(1)

    master.to_csv('nevadagrown_master.csv', index = False)




# nevada_grown()

