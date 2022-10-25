import pandas as pd
import numpy as np
import sys, os , time


# old = pd.read_csv('old_crm.csv')
# confList = pd.read_excel('2021_almond_conf_contact_list.xlsx')

def phone_email_compare():
    phoneDf, email = old[['Phone', 'MobilePhone', 'Phone_Alt__c', 'cell__c', 'Fax__c']].values, old['Email']
    phones = []
    for l in phoneDf:
        phones+=list(l)

    phones = [str(c).replace('-', '').replace('.', '').replace('(','').replace(')','').replace(' ', '').strip() for c in phones if str(c) != 'nan']
    email = [str(c).lower().strip() for c in email]
    p = [c for c in phones if len(c) != 10]
    newPhones = confList['Phone Number']
    print([str(c).lstrip('+1') for c in newPhones])
    sys.exit()
    for i, n in enumerate(newPhones):
        n = str(n)
        if n[:2] == '+1':
            newPhones[i] = n[2:].replace('-', '').strip()
        else:
            newPhones[i] = n

    newFax = confList['Fax Number']
    newFax = [str(c).replace('-', '').replace('.', '').strip() for c in newFax]
    newEmails = confList['Email']

    matches = {'phone': [],
               'fax' : [],
               'email' : []}
    new = {'phone': [],
           'fax' : [],
           'email': []}

    removal = []
    for i, data in enumerate([newPhones, newFax, newEmails]):
        for n,d in enumerate(data):
            if i == 0:
                if d in phones:
                    removal.append(n)
                    matches['phone'].append(d)
                else:
                    new['phone'].append(d)
            elif i == 1:
                if d in phones:
                    removal.append(n)
                    matches['fax'].append(d)
                else:
                    new['fax'].append(d)
            elif i == 2:
                if d.lower().strip() in email:
                    removal.append(n)
                    matches['email'].append(d)
                else:
                    new['email'].append(d)

    print('MATCHES')
    for name, data in matches.items():
        print(name + '  :  ' + str(len(data)))

    print('NEW')
    for name, data in new.items():
        print(name + '  :  ' + str(len(data)))

    confList.drop(removal, axis=0, inplace = True)
    confList['full address'] = np.zeros_like(confList['Address'])
    for row in confList.iterrows():
        i, row = row
        confList.loc[i, 'full address'] = str(row['Address']) + ', ' + str(row['City']) + ', ' + str(row['State']) + ', '  + str(row['Zip Code'])
    confList.to_csv('2021_almond_conf_contact_list_filtered.csv', index = False)

# phone_email_compare()
def name_compare():
    newNames = np.array([str(c).strip() for c in confList['First Name']]) + np.ones_like(confList['First Name']) * ' ' +  np.array([str(c).strip() for c in confList['Last Name']])
    newNames = [c.lower() for c in list(newNames)]
    oldNames = np.array([str(c).strip() for c in old['FirstName']]) + np.ones_like(old['FirstName']) * ' ' +  np.array([str(c).strip() for c in old['LastName']])
    oldNames = [c.lower() for c in list(oldNames)]

    matches = []
    new = []
    for n in newNames:
        if n in oldNames:
            matches.append(n)
        else:
            new.append(n)
    print('MATCHES')
    print(len(matches))
    print('NEW')
    print(len(new))

def company_compare():
    newComp = [str(c).lower().strip() for c in confList['Company Name']]
    oldComp = [str(c).lower().strip() for c in old['Company']]

    matches = []
    new = []
    for n in newComp:
        if n in oldComp:
            matches.append(n)
        else:
            new.append(n)
    print('MATCHES')
    print(len(matches))
    print('NEW')
    print(len(new))

# title = confList['Title'].apply(lambda x: x.lower().strip())
# d = pd.DataFrame(title.unique())
# d.to_csv('job_titles.csv', index = False)

# data = pd.read_csv('2021_almond_conf_contact_list_filtered.csv')
#
# phones = data['Phone Number']
# nphone = []
# for p in phones:
#     try:
#         nphone.append(str(int(p)))
#     except:
#         pass
#
# short = [c for c in nphone if len(c)<10]
# print(len(short))

def filter_by_title(titles):
    data = pd.read_csv('2021_almond_conf_contact_list_filtered.csv')
    data['Title'] = data['Title'].apply(lambda x: x.lower())
    newData = pd.DataFrame()
    for t in titles:
        newData = newData.append(data[data['Title'] == t])
    newData.to_excel('almond_conf_list_relevantTitles.xlsx', index=  False)
    lengths = []
    for g in newData.groupby('Company Name'):
        g,dat=g
        lengths.append(len(dat))

# titlelist = pd.read_csv('job_titles_filtered.csv')
# titles = titlelist['New']
# filter_by_title(titles)

def mailing_list(filepath):
    data = pd.read_csv('crm_9242021.csv')
    old = pd.DataFrame()
    for ind in ['Cherries','Blueberry']:
        old = old.append(data[data['Industry'] == ind])
    print(old)
    sys.exit()
    old = data[data['Industry'] == 'Almond']
    conf = data[data['Industry'] == 'Tree Nut Farming']
    oldMail = pd.DataFrame()
    confMail = pd.DataFrame()
    for row in old.iterrows():
        i, row = row
        fullAdd = ''
        for add in ['Street', 'City', 'State', 'PostalCode']:
            if type(row[add]) == str:
                fullAdd = fullAdd + row[add].strip() + ', ' if add != 'PostalCode' else fullAdd + row[add].strip()
        fullAdd = fullAdd.strip()
        # fullAdd = (row['Street'].strip() + ', ' + row['City'].strip() + ', ' + row['State'].strip() + ' ' + row['PostalCode']).strip()
        oldMail = oldMail.append({'FirstName' : str(row['FirstName']).strip(),
                        'LastName' : str(row['LastName']).strip(),
                        'Company': str(row['Company']).strip(),
                        'Full Address': fullAdd,
                        'Street': str(row['Street']).strip(),
                        'City': str(row['City']).strip(),
                        'State' : str(row['State']).strip(),
                        'Zip' : str(row['PostalCode']).strip()}, ignore_index=True)

    for row in conf.iterrows():
        i, row = row
        fullAdd = ''
        for add in ['Street', 'City', 'State', 'PostalCode']:
            if type(row[add]) == str:
                fullAdd = fullAdd + row[add].strip() + ', ' if add != 'PostalCode' else fullAdd + row[add].strip()
        fullAdd = fullAdd.strip()
        # fullAdd = (row['Street'].strip() + ', ' + row['City'].strip() + ', ' + row['State'].strip() + ' ' + row['PostalCode']).strip()
        confMail = confMail.append({'FirstName' : str(row['FirstName']).strip(),
                        'LastName' : str(row['LastName']).strip(),
                        'Company': str(row['Company']).strip(),
                        'Full Address': fullAdd,
                        'Street': str(row['Street']).strip(),
                        'City': str(row['City']).strip(),
                        'State' : str(row['State']).strip(),
                        'Zip' : str(row['PostalCode']).strip()}, ignore_index=True)

    # oldMail.to_csv('oldCRM_mailing_list.csv', index=False)
    confMail.to_csv('conference_mailing_list.csv', index=False)

# mailing_list('crm_9242021.csv')

def add_crops(crops):
    master = pd.read_csv('combinedCRM_mailing_list.csv')
    cropData = pd.read_csv('full_master.csv')
    cropData=cropData[['Operator', 'Mailing Address','City','State','Zip', 'Commodity']]
    for crop in crops:
        fname = []
        lname = []
        currCrop = cropData[cropData['Commodity'] == crop]
        currCrop['Company'] = currCrop['Operator']
        currCrop['FullName'] = currCrop['Operator']
        splitNames = currCrop['Operator'].apply(lambda x: str(x).split(' '))
        for n in splitNames:
            if len(n) == 2:
                fname.append(n[0].strip(','))
                lname.append(n[1])
            else:
                fname.append(np.nan)
                lname.append(np.nan)
        currCrop['FirstName'] = fname
        currCrop['LastName'] = lname
        currCrop['Street'] = currCrop.copy()['Mailing Address'].apply(lambda x: str(x).split(',')[0])
        currCrop.rename({'Mailing Address':'Full Address',
                         'Commodity':'Crop'}, axis = 1,inplace = True)
        currCrop = currCrop[['FirstName', 'LastName', 'Company', 'Full Address','Street', 'City', 'State', 'Zip','FullName','Crop']]
        uniqueAdds = list(currCrop['Full Address'].unique())
        drops = []
        for row in currCrop.iterrows():
            i,row = row
            if row['Full Address'] in uniqueAdds:
                uniqueAdds.remove(row['Full Address'])
            else:
                drops.append(i)
        currCrop.drop(drops, axis = 0 ,inplace=True)
        master = master.append(currCrop)
    master.to_csv('threeCrop_mailinglist.csv', index = False)
add_crops(['BLUEBERRY', 'CHERRY'])